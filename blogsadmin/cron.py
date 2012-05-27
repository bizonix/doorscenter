# coding=utf8
from django.db.models import Max
from django.core.mail import send_mail
from blogsadmin.models import Blog, Position
import datetime

def CronHourly():
    '''Функция вызывается по расписанию'''
    CheckBlogs()
    CheckPositions()

def CheckBlogs():
    '''Проверяем блоги'''
    lastChecked = Blog.objects.all().aggregate(x=Max('lastChecked'))['x']
    delta = datetime.datetime.now() - lastChecked
    if (delta.days * 24 * 60 * 60 + delta.seconds) / 60 < 55:  # настройка: интервал парсинга в минутах
        return
    blogs = Blog.objects.order_by('lastChecked', 'pk').all()
    for blog in blogs[:10]:  # настройка
        blog.Check()

def CheckPositions():
    '''Проверяем позиции'''
    lastChecked = Position.objects.all().aggregate(x=Max('lastChecked'))['x']
    delta = datetime.datetime.now() - lastChecked
    if (delta.days * 24 * 60 * 60 + delta.seconds) / 60 < 55:  # настройка: интервал парсинга в минутах
        return
    news = ''
    positions = Position.objects.order_by('lastChecked', 'pk').all()
    for position in positions[:25]:  # настройка
        googlePositionOld = position.googlePosition
        yahooPositionOld = position.yahooPosition
        bingPositionOld = position.bingPosition
        position.Check()
        googlePositionNew = position.googlePosition
        yahooPositionNew = position.yahooPosition
        bingPositionNew = position.bingPosition
        if (googlePositionOld > 10 and googlePositionNew <= 10) or (yahooPositionOld > 10 and yahooPositionNew <= 10) or (bingPositionOld > 10 and bingPositionNew <= 10):
            news += '%s gain;' % position
        if (googlePositionOld <= 10 and googlePositionNew > 10) or (yahooPositionOld <= 10 and yahooPositionNew > 10) or (bingPositionOld <= 10 and bingPositionNew > 10):
            news += '%s lost;' % position
    if news != '':
        send_mail('Blogs Administration', news, 'alex@searchpro.name', ['alex@altstone.com'], fail_silently = True)
