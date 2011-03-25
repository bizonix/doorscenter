# coding=utf8
from django.core.management.base import BaseCommand
from doorsadmin.models import DoorwaySchedule, SnippetsSet, Agent, EventLog
from doorsadmin.common import *
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        dd = datetime.date.today()
        dt = datetime.datetime.now()
        '''Генерируем дорвеи'''
        for p in DoorwaySchedule.objects.filter(active=True).all(): 
            if (p.dateStart <= dd) and ((p.dateEnd==None) or (p.dateEnd >= dd)):
                p.GenerateDoorways()
        '''Сниппеты'''
        for p in SnippetsSet.objects.filter(active=True).all():
            if (p.dateLastParsed==None) or (p.dateLastParsed + datetime.timedelta(0, p.interval*60*60, 0) < dt):
                p.stateManaged = 'new'
                p.save()
        '''Проверяем активность агентов'''
        for p in Agent.objects.filter(active=True).all():
            if (p.dateLastPing!=None) and (p.dateLastPing + datetime.timedelta(0, p.interval*60*60, 0) < dt):
                EventLog('error', 'Agent long inactivity', p, None)
        '''Конец'''
        self.stdout.write('Done\n')
