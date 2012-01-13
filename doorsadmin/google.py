# coding=utf8
import re, tempfile

url_home = 'http://www.google.com/'
url_search = 'http://www.google.com/search?hl=en&q=%s&btnG=Google+Search'
cookie_name = '.google-cookie'

def GetPagesCount(html):
    '''Из текста страницы получаем количество найденных страниц'''
    return int(re.findall(r'of about <b>([0-9,]*)</b>', html)[0].replace(',', ''))

###

import os, cookielib, urllib, urllib2

cookie_jar = cookielib.LWPCookieJar(os.path.join(tempfile.gettempdir(), cookie_name))
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

def GetIndexLink(siteName):
    return url_search % urllib.quote_plus('site:' + siteName)

def GetIndex(siteName):
    pages = 0
    try:
        html = GetPage(GetIndexLink(siteName))
        pages = GetPagesCount(html)
    except Exception:
        pass
    return pages

if __name__ == '__main__':
    Initialize()
    print(GetIndex('mail.ru'))
    print(GetIndex('ssecure.info'))
