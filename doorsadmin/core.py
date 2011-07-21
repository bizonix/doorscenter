# coding=utf8
from django.db.models import Q
from doorsadmin.models import Net, SnippetsSet, DoorwaySchedule, Niche, Agent, Event, EventLog
import datetime

def CronHourly():
    '''Функция вызывается по расписанию'''
    GenerateSnippets()
    #GenerateNets()
    GenerateDoorways()
    CheckAgentsActivity()

def CronDaily():
    '''Функция вызывается по расписанию'''
    GenerateSpamTasks()
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
    for net in Net.objects.filter(active=True).all():
        net.UpdateNet()

def GenerateDoorways():
    '''Генерируем дорвеи'''
    dd = datetime.date.today()
    for schedule in DoorwaySchedule.objects.filter(active=True).all():
        if (schedule.dateStart <= dd) and ((schedule.dateEnd==None) or (schedule.dateEnd >= dd)):
            schedule.GenerateDoorways()

def GenerateSpamTasks():
    '''Генерируем задания для спама'''
    for niche in Niche.objects.filter(active=True).all():
        niche.GenerateSpamTasksChip()

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
