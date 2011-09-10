# coding=utf8
__version__ = "$Id: google.py 759 2010-07-16 15:27:53Z qvasimodo $"

import cookielib
import os
import urllib
import urllib2
import re

# URL templates to make Google searches.
url_home          = "http://www.google.%(tld)s/"
url_search        = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&btnG=Google+Search"
url_next_page     = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&start=%(start)d"
url_search_num    = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&btnG=Google+Search"
url_next_page_num = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&start=%(start)d"

# Cookie jar. Stored at the user's home folder.
cookie_jar = cookielib.LWPCookieJar(os.path.join(os.getenv('HOME'), '.google-cookie'))
try:
    cookie_jar.load()
except Exception:
    pass

# Request the given URL and return the response page, using the cookie jar
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

def GetIndex(siteName, tld='com', lang='en'):
    query = urllib.quote_plus('site:' + siteName)
    try:
        GetPage(url_home % vars())
        html = GetPage(url_search % vars())
        n = re.findall(r"About ([0-9,]*) results", html)[0]
        n = int(n.replace(',', ''))
    except Exception:
        n = 0
    return n

if __name__ == "__main__":
    print(GetIndex('mail.ru'))
    print(GetIndex('ssecure.info'))
