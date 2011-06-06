# coding=utf8
from django.db.models import Q
from doorsadmin.models import SnippetsSet, Domain, DoorwaySchedule, Niche, SpamLink, Agent, Event, EventLog
import datetime

def Cron():
    '''Функция вызывается по расписанию'''
    #GenerateSnippets()  # фича пока отключена из-за бана парсера гуглом
    GenerateNets()
    GenerateDoorways()
    GenerateSpamTasks()
    CheckAgentsActivity()
    ClearEventLog()

def GenerateSnippets():
    '''Перегенерируем сниппеты'''
    dt = datetime.datetime.now()
    for snippetsSet in SnippetsSet.objects.filter(Q(active=True), Q(stateManaged='done')).all():
        if (snippetsSet.dateLastParsed==None) or (snippetsSet.dateLastParsed + datetime.timedelta(0, snippetsSet.interval*60*60, 0) < dt):
            snippetsSet.stateManaged = 'new'
            snippetsSet.save()

def GenerateNets():
    '''Плетем сети'''
    for domain in Domain.objects.filter(~Q(net=None), Q(maxLinkedDomains=None), Q(active=True)).all(): 
        domain.net.AddDomain(domain)
        domain.save()

def GenerateDoorways():
    '''Генерируем дорвеи'''
    dd = datetime.date.today()
    for schedule in DoorwaySchedule.objects.filter(active=True).all(): 
        if (schedule.dateStart <= dd) and ((schedule.dateEnd==None) or (schedule.dateEnd >= dd)):
            schedule.GenerateDoorways()

def GenerateSpamTasks():
    '''Генерируем задания для спама'''
    for niche in Niche.objects.filter(active=True).all(): 
        niche.GenerateSpamTasks()
    print('Spam links unallocated: %d.' % SpamLink.objects.filter(spamTask=None).count())

def CheckAgentsActivity():
    '''Проверяем активность агентов'''
    dt = datetime.datetime.now()
    for agent in Agent.objects.filter(active=True).all():
        if (agent.stateSimple == 'ok') and (agent.dateLastPing != None) and (agent.dateLastPing + datetime.timedelta(0, agent.interval*60*60, 0) < dt):
            EventLog('error', 'Agent long inactivity', agent)
            agent.stateSimple = 'error'
            agent.save()

def ClearEventLog():
    '''Удаляем старые записи из лога событий'''
    dt = datetime.datetime.now() - datetime.timedelta(30)  # старше 30 дней
    Event.objects.filter(date__lt=dt).delete()
