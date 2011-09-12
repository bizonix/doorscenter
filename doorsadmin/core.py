# coding=utf8
from django.db.models import Q
from doorsadmin.models import Net, SnippetsSet, XrumerBaseR, Agent, Event, EventLog
import datetime

def CronHourly():
    '''Функция вызывается по расписанию'''
    RenewSnippets()
    RenewBasesR()
    CheckAgentsActivity()

def CronDaily():
    '''Функция вызывается по расписанию'''
    GenerateNets()
    #GenerateDoorways()  # дорвеи генерируются при добавлении домена в сеть
    #GenerateSpamTasks()  # вызывается по событию апдейта агента доргена
    ClearEventLog()

def Helper():
    '''Запуск из командной строки'''
    pass
    
def GenerateNets():
    '''Плетем сети'''
    spamTasksLimit = 100  # настройка
    linksLimitBase = spamTasksLimit * 12
    linksLimitActual = linksLimitBase
    dd = datetime.date.today()
    for net in Net.objects.filter(active=True).order_by('pk').all():
        if (net.domainsPerDay > 0) and ((net.dateStart==None) or (net.dateStart <= dd)) and ((net.dateEnd==None) or (net.dateEnd >= dd)):
            linksLimitActual = net.AddDomains(None, linksLimitActual)
        if linksLimitActual <= 0:
            break
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

def ClearEventLog():
    '''Удаляем старые записи из лога событий'''
    dt = datetime.datetime.now() - datetime.timedelta(30)  # старше 30 дней
    Event.objects.filter(date__lt=dt).delete()
