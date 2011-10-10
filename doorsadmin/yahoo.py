# coding=utf8
import re

url_home = 'http://www.yahoo.com/'
url_search = 'http://siteexplorer.search.yahoo.com/search?p=%s&bwm=i&bwmf=s&bwmo=&fr=yfp-t-701&fr2=seo-rd-se'
cookie_name = '.yahoo-cookie'

def GetBackLinksCount(html):
    '''Из текста страницы получаем количество обратных ссылок'''
    html = html.replace('<strong>', '')
    html = html.replace('</strong>', '')
    return int(re.findall(r'Showing[ 0-9,]*to[ 0-9,]*of([ 0-9,]*)', html)[0].replace(',', '').replace(' ', ''))

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

def GetBackLinks(siteName):
    pages = 0
    try:
        html = GetPage(url_search % urllib.quote_plus(siteName))
        pages = GetBackLinksCount(html)
    except Exception:
        pass
    return pages

if __name__ == '__main__':
    Initialize()
    print(GetBackLinks('mail.ru'))
    print(GetBackLinks('ssecure.info'))
