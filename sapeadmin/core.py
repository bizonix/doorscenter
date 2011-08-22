# coding=utf8
#from django.db.models import Q
from sapeadmin.models import Site, YandexUpdate
import urllib, re, datetime

def CronDaily():
    '''Функция вызывается по расписанию'''
    CheckBotVisits()
    CheckYandexUpdates()
    print('done')

def CronHourly():
    '''Функция вызывается по расписанию'''
    print('done')

def CheckBotVisits():
    '''Проверка захода ботов'''
    for site in Site.objects.filter(state='spam-indexed').order_by('pk').all():
        fd = urllib.urlopen('%sbots.php' % site.url)
        visitsCount = 0
        try:
            visitsCount = int(re.search(r'<b>(\d*)</b>', fd.read(), re.MULTILINE).group(1))
        except Exception:
            pass
        fd.close()
        site.botsVisitsCount = visitsCount
        if (site.botsVisitsDate == None) and (float(visitsCount) / site.pagesCount >= 0.85):
            site.botsVisitsDate = datetime.datetime.now()
        if visitsCount >= site.pagesCount:
            site.state = 'bot-visited'
        site.save()

def CheckYandexUpdates():
    '''Парсинг апдейтов яндекса'''
    fd = urllib.urlopen('http://tools.promosite.ru/updates/')
    update = ''
    try:
        update = re.search(u'Текстовый апдейт: выложен индекс по (.*)<br>', fd.read().decode('cp1251'), re.UNICODE).group(1)
    except Exception:
        pass
    fd.close()
    update = update.replace(u' января ', '.01.')
    update = update.replace(u' февраля ', '.02.')
    update = update.replace(u' марта ', '.03.')
    update = update.replace(u' апреля ', '.04.')
    update = update.replace(u' мая ', '.05.')
    update = update.replace(u' июня ', '.06.')
    update = update.replace(u' июля ', '.07.')
    update = update.replace(u' августа ', '.08.')
    update = update.replace(u' сентября ', '.09.')
    update = update.replace(u' октября ', '.10.')
    update = update.replace(u' ноября ', '.11.')
    update = update.replace(u' декабря ', '.12.')
    if len(update) == 9:
        update = '0' + update
    update = update[6:10] + '-' + update[3:5] + '-' + update[0:2]
    try:
        YandexUpdate.objects.create(dateUpdate=datetime.datetime.now(), dateIndex=update).save()
    except Exception:
        pass
