# coding=utf8
from django.core.management.base import BaseCommand
from doorsadmin.models import Doorway, SpamLink, SpamTask
import re

class Command(BaseCommand):
    def _FillSpamLinks(self):
        '''Задание для миграции: заполняем таблицу ссылок для спама'''
        SpamLink.objects.all().delete()
        xlinks = {}
        '''Цикл по заданиям'''
        for spamTask in SpamTask.objects.all():
            for link in spamTask.spamLinksList.split('\n'):
                link = link.strip()
                xlinks[link] = spamTask
        '''Цикл по дорам'''
        rxHtml = re.compile(r'<a href="(.*)">(.*)</a>')
        for doorway in Doorway.objects.all():
            for link in doorway.spamLinksList.split('\n'):
                '''Парсим'''
                link = link.strip()
                x = rxHtml.match(link)
                if not x:
                    continue
                if len(x.groups()) != 2:
                    continue
                url = x.groups()[0]
                anchor = x.groups()[1]
                spamTask = None
                if link in xlinks:
                    spamTask = xlinks[link]
                '''Создаем ссылки'''
                SpamLink.objects.create(url=url, anchor=anchor, doorway=doorway, spamTask=spamTask).save()
                if url.endswith('/index.html'):
                    url = url.replace('/index.html', '/sitemap.html')
                    SpamLink.objects.create(url=url, anchor=anchor, doorway=doorway).save()
    
    def handle(self, *args, **options):
        self._FillSpamLinks()
        self.stdout.write('Done\n')
