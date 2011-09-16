# coding=utf8
from django.db.models import Q
from doorsadmin.models import Niche, Net, Domain, SnippetsSet, XrumerBaseR, Agent, Event, EventLog
import datetime

def CronHourly():
    '''Функция вызывается по расписанию'''
    RenewSnippets()
    RenewBasesR()
    CheckAgentsActivity()

def CronDaily():
    '''Функция вызывается по расписанию'''
    ExpandNets()
    #GenerateDoorways()  # дорвеи генерируются при добавлении домена в сеть
    #GenerateSpamTasks()  # вызывается по событию апдейта агента доргена
    ClearEventLog()

def Helper():
    '''Запуск из командной строки'''
    for niche in Niche.objects.filter(active=True).order_by('pk').all():
        niche.GenerateSpamTasksMultiple()
    
def ExpandNets():
    '''Плетем сети'''
    avgSpamTaskDuration = 15  # настройка: средняя продолжительность прогона по базе R, минут
    avgSpamLinksPerTask = 12  # настройка: среднее количество ссылок в задании на спам
    domainsLimitBase = 20  # настройка: лимит расхода доменов в сутки
    linksLimitBase = int(1440 * 0.9 / avgSpamTaskDuration * avgSpamLinksPerTask)  # максимум ссылок, которые можно проспамить за сутки
    domainsLimitActual = domainsLimitBase
    linksLimitActual = linksLimitBase
    dd = datetime.date.today()
    for net in Net.objects.filter(active=True).order_by('?').all():
        if (net.domainsPerDay > 0) and ((net.dateStart==None) or (net.dateStart <= dd)) and ((net.dateEnd==None) or (net.dateEnd >= dd)):
            domainsLimitActual, linksLimitActual = net.AddDomains(None, linksLimitActual)
        if (domainsLimitActual <= 0) or (linksLimitActual <= 0):
            break
    EventLog('info', 'Domains limit: %d/%d' % (domainsLimitBase - domainsLimitActual, domainsLimitBase))
    EventLog('info', 'Links limit: %d/%d' % (linksLimitBase - linksLimitActual, linksLimitBase))

def RenewSnippets():
    '''Перегенерируем сниппеты'''
    dt = datetime.datetime.now()
    for snippetsSet in SnippetsSet.objects.filter(Q(active=True), Q(stateManaged='done')).order_by('pk').all():
        if (snippetsSet.dateLastParsed==None) or (snippetsSet.dateLastParsed + datetime.timedelta(0, snippetsSet.interval*60*60, 0) < dt):
            snippetsSet.stateManaged = 'new'
            snippetsSet.save()

def RenewBasesR():
    '''Перегенерируем изношенные базы'''
    for xrumerBaseR in XrumerBaseR.objects.filter(Q(active=True), Q(stateManaged='done')).order_by('pk').all():
        if xrumerBaseR.linksCount < 2:  # в тысячах
            xrumerBaseR.stateManaged = 'new'
            xrumerBaseR.save()

def CheckAgentsActivity():
    '''Проверяем активность агентов'''
    dt = datetime.datetime.now()
    for agent in Agent.objects.filter(active=True).order_by('pk').all():
        if (agent.stateSimple == 'ok') and (agent.dateLastPing != None) and (agent.dateLastPing + datetime.timedelta(0, agent.interval*60*60, 0) < dt):
            EventLog('error', 'Agent long inactivity', agent)
            agent.stateSimple = 'error'
            agent.save()

def CheckOwnershipTk():
    '''Проверяем .tk на отбор'''
    processed = 0
    failed = 0
    for domain in Domain.objects.filter(Q(stateSimple='ok'), Q(name__contains='.tk')):
        if not domain.CheckOwnership():
            failed += 1
            print(domain)
        processed += 1
    print("%d checked, %d failed." % (processed, failed))

def ClearEventLog():
    '''Удаляем старые записи из лога событий'''
    dt = datetime.datetime.now() - datetime.timedelta(30)  # старше 30 дней
    Event.objects.filter(date__lt=dt).delete()
