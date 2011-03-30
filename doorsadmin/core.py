# coding=utf8
from django.db.models import Q
from doorsadmin.models import XrumerBaseR, Doorway, SpamTask, DoorwaySchedule, SnippetsSet, Agent, Event, EventLog
import random, datetime

def Cron():
    '''Функция вызывается по расписанию'''
    GenerateSnippets()
    GenerateDoorways()
    GenerateSpamTasks()
    CheckAgentsActivity()
    ClearEventLog()

def GenerateSnippets():
    '''Собираем сниппеты'''
    dt = datetime.datetime.now()
    for p in SnippetsSet.objects.filter(active=True).all():
        if (p.dateLastParsed==None) or (p.dateLastParsed + datetime.timedelta(0, p.interval*60*60, 0) < dt):
            p.stateManaged = 'new'
            p.save()

def GenerateDoorways():
    '''Генерируем дорвеи'''
    dd = datetime.date.today()
    for p in DoorwaySchedule.objects.filter(active=True).all(): 
        if (p.dateStart <= dd) and ((p.dateEnd==None) or (p.dateEnd >= dd)):
            p.GenerateDoorways()

def GenerateSpamTasks():
    '''Генерируем задания для спама. Постановка задачи:
    1. каждый дор прогонять по заданиям до 2 раз. сначала прогонять доры с нулевым числом заданий, затем с одним и т.д.
    2. дор должен прогоняться по базе р своей ниши.
    3. один домен по одной базе должен прогоняться не чаще, чем через 9 прогонов.
    4. в одном задании может быть только одна база р, соответственно только одна ниша.
    5. в одном задании может быть несколько доров. должно быть 2-4 разных домена, от каждого дора 3-5 ссылок.'''
    '''Сначала спамим не проспамленные доры, затем проспамленные 1 раз и т.д.'''
    for spamCounter in range(1): 
        '''Цикл по активным готовым базам'''
        for xrumerBaseR in XrumerBaseR.objects.filter(Q(active=True), Q(stateManaged='done')).order_by('?').all(): 
            doorwaysList = []  # доры для задания
            spamLinksList = []  # ссылки доров для задания
            domainsList = []  # домены задания
            domainsCount = random.randint(2, 4)  # сколько разных доменов будем включать в это задание
            '''Цикл по готовым дорвеям, у которых ниша совпадает с нишей базы'''
            for doorway in Doorway.objects.filter(Q(niche=xrumerBaseR.niche), Q(stateManaged='done')).order_by('pk').all(): 
                if doorway.spamtask_set.count() > spamCounter:  # отсекаем доры по количеству заданий
                    continue
                if doorway.domain in domainsList:  # отсекаем доры, чьи домены уже есть в задании
                    continue
                if xrumerBaseR.GetDomainPosition(doorway.domain) < 10:  # отсекаем доры, чьи домены спамились по базе < 10 раз назад
                    continue
                '''Дор, прошедший отбор, добавляем в список'''
                doorwaysList.append(doorway) 
                doorwayLinksList = doorway.spamLinksList.split('\n')  # берем случайный список страниц дора для спама
                random.shuffle(doorwayLinksList)
                spamLinksList.extend(doorwayLinksList[:random.randint(3, 5)])
                domainsList.append(doorway.domain)
                '''Создаем задание'''
                if len(domainsList) >= domainsCount:
                    spamTask = SpamTask.objects.create(xrumerBaseR=xrumerBaseR, spamLinksList='\n'.join(spamLinksList))
                    for doorway in doorwaysList:
                        spamTask.doorways.add(doorway)
                    spamTask.save()
                    '''Обнуляем переменные'''
                    doorwaysList = []  # доры для задания
                    spamLinksList = []  # ссылки доров для задания
                    domainsList = []  # домены задания
                    domainsCount = random.randint(2, 4)  # сколько разных доменов будем включать в это задание

def CheckAgentsActivity():
    '''Проверяем активность агентов'''
    dt = datetime.datetime.now()
    for p in Agent.objects.filter(active=True).all():
        if (p.stateSimple == 'ok') and (p.dateLastPing != None) and (p.dateLastPing + datetime.timedelta(0, p.interval*60*60, 0) < dt):
            EventLog('error', 'Agent long inactivity', p)
            p.stateSimple = 'error'
            p.save()

def ClearEventLog():
    '''Удаляем старые записи из лога событий'''
    dt = datetime.datetime.now() - datetime.timedelta(30)  # старше 30 дней
    Event.objects.filter(date__lt=dt).delete()
