# coding=utf8
import re

url_home = 'http://www.yandex.ru/'
url_search = 'http://yandex.ru/yandsearch?text=%s&lr=2'
cookie_name = '.yandex-cookie'

def GetPagesCount(html):
    '''Из текста страницы получаем количество найденных страниц'''
    return int(re.findall(r'<title>.*Яндекс\:[^\d]*(\d*).*</title>', html, re.M | re.U | re.S)[0].replace(',', ''))

###

import os, cookielib, urllib, urllib2

cookie_jar = cookielib.LWPCookieJar(os.path.join('/home/sasch', cookie_name))
try:
    cookie_jar.load()
except Exception:
    pass

def GetPage(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
    cookie_jar.add_cookie_header(request)
    response = urllib2.urlopen(request)
    cookie_jar.extract_cookies(response, request)
    html = response.read()
    response.close()
    cookie_jar.save()
    return html

def Initialize():
    try:
        GetPage(url_home)
        return True
    except Exception:
        return False

def GetIndex(siteName):
    pages = 0
    try:
        html = GetPage(url_search % urllib.quote_plus('site:' + siteName))
        pages = GetPagesCount(html)
    except Exception:
        pass
    return pages

if __name__ == '__main__':
    Initialize()
    print(GetIndex('mail.ru'))
    print(GetIndex('patefon.knet.ru'))
    print(GetIndex('balkan.ru'))
