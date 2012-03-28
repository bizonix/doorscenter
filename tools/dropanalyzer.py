# coding=utf8

import os, re, random, cookielib, tempfile, datetime, urllib, urllib2

'''
Для сайтов по списку возвращает:
- число страниц в гугле;
- число бэков в гугле, и их список;
- ссылку на одну страницу из кэша гугла.
'''

class DropAnalyzer(object):
    '''Анализ списка дропов'''
    
    def __init__(self):
        '''Инициализация'''
        self.pause = 5  # время между запросами в секундах
        self.resultsList = [r'About ([0-9,]*) res', r'of about <b>([0-9,]*)</b>', r'<div>([0-9,]*) res']
        self.rxResultsList = [re.compile(item) for item in self.resultsList]
        self.userAgentsList = '''Opera/10.00 (Windows NT 5.1; U; ru) Presto/2.2.0
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.2; OfficeLiveConnector.1.3; OfficeLivePatch.0.0; .NET CLR 3.5.30729; .NET CLR 3.0.30618)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 1.1.4322; InfoPath.1)
Opera/9.62 (Windows NT 5.1; U; ru) Presto/2.1.1
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; GTB5; MRSPUTNIK 2, 0, 1, 31 SW; MRA 5.2 (build 02415); .NET CLR 1.1.4322; InfoPath.2; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)
Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 1.1.4322)
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FunWebProducts; (R1 1.5); .NET CLR 1.1.4322)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; FunWebProducts; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.1)
Mozilla/5.0 (Windows; U; Windows NT 5.1; pl; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1)
Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11
Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.8.0.6) Gecko/20060728 Firefox/1.5.0.6
Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)
Opera/9.25 (Windows NT 5.1; U; pl)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; AT&amp;T CSM6.0; .NET CLR 1.1.4322)
Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.7) Gecko/20060909 Firefox/1.5.0.7
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FDM)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.04506.30; InfoPath.2)
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; .NET CLR 2.0.50727)
Opera/9.20 (Windows NT 5.1; U; ru)
Opera/9.23 (Windows NT 5.1; U; ru)
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FileDownloader; .NET CLR 1.0.3705; .NET CLR 1.1.4322; InfoPath.1; FileDownloader; Media Center PC 4.0; .NET CLR 2.0.50727; MEGAUPLOAD 2.0)
Opera/9.21 (Windows NT 5.0; U; ru)
Opera/9.25 (Windows NT 5.1; U; bg)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; PeoplePal 3.0)
Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1); afcid=Wadf57d6951da76af4c6f0b08181c298d
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; MEGAUPLOAD 2.0)
Opera/8.54 (Windows NT 5.1; U; ru)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; YComp 5.0.0.0; .NET CLR 1.0.3705; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648)SAMSUNG-SGH-P910/1.0 SHP/VPP/R5 NetFront/3.3 SMM-MMS/1.2.0 profile/MIDP-2.0 configuration/CLDC-1.1
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; ADVPLUGIN|K115|165|S548873517|dial; 666XXX040507; .NET CLR 2.0.50727)'''.split('\n')
        self.cookieJar = cookielib.LWPCookieJar(os.path.join(tempfile.gettempdir(), '.google-cookie'))
    
    def Process(self, domainsList, fileName):
        '''Парсинг доменов'''
        print('Parsing domains ...')
        dateTimeStart = datetime.datetime.now()
        cacheLinks = ''
        for domain in domainsList:
            try:
                domain = domain.strip()
                '''Делаем запрос'''
                url = 'http://www.google.com/search?hl=en&q=%s&btnG=Google+Search' % (urllib.quote_plus(domain))
                request = urllib2.Request(url)
                request.add_header('User-Agent', random.choice(self.userAgentsList))
                self.cookieJar.add_cookie_header(request)
                response = urllib2.urlopen(request)
                html = response.read()
                response.close()
                '''Парсим ответ'''
                count = None
                for rx in self.rxResultsList:
                    try:
                        count = int(rx.findall(html)[0].replace(',', ''))
                    except Exception:
                        pass
                if count != None:
                    print('- %s: %d' % (domain, count))
                    if count > 0:
                        cacheLinks += '<a href="http://www.google.com/search?hl=en&q=cache:%s&btnG=Google+Search" target="_blank">%s</a> \n' % (domain, domain)
                else:
                    print('Error counting')
            except Exception:
                pass
        open(fileName, 'w').write(cacheLinks)
        print('Parsed %d domains in %d sec.' % (len(domainsList), (datetime.datetime.now() - dateTimeStart).seconds))

if __name__ == '__main__':
    DropAnalyzer().Process(['mail.ru', 'lenta.ru'], r'c:\Temp\8\drops.html')
