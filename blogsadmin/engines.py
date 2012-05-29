# coding=utf8
import pycurl, cStringIO, random, urllib, re

proxyUrls = ['174.127.67.236:554', '206.217.201.28:554', '206.217.201.30:554']
proxyUser = '218660178:dd7a0e1e'

class Engine(object):
    '''Предок используемых сайтов'''
    
    @classmethod
    def GetPage(self, url):
        '''Читаем урл и возвращаем текст'''
        try:
            buf = cStringIO.StringIO()
            curl = pycurl.Curl()
            curl.setopt(pycurl.HTTPHEADER, ["Accept:"])
            curl.setopt(pycurl.USERAGENT, 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
            curl.setopt(pycurl.FOLLOWLOCATION, 1)
            curl.setopt(pycurl.MAXREDIRS, 5)
            curl.setopt(pycurl.CONNECTTIMEOUT, 10)
            curl.setopt(pycurl.TIMEOUT, 10)
            curl.setopt(pycurl.PROXY, random.choice(proxyUrls))
            curl.setopt(pycurl.PROXYUSERPWD, proxyUser)
            curl.setopt(pycurl.URL, url)
            curl.setopt(pycurl.WRITEFUNCTION, buf.write)
            curl.perform()
            return buf.getvalue()
        except Exception:
            return ''
        
    @classmethod
    def GetLink(self, url, item):
        '''Возвращаем ссылку'''
        return url % urllib.quote_plus(item.encode('cp1251'))
    
    @classmethod
    def GetIndex(self, domain, regexpsList):
        '''Получаем индекс'''
        html = self.GetPage(self.GetIndexLink(domain))
        for indexRegexp in regexpsList:
            try:
                return int(re.findall(indexRegexp, html)[0].replace(',', ''))
            except Exception:
                pass
        return 0
    
    @classmethod
    def GetBackLinks(self, domain, regexpsList):
        '''Получаем обратные ссылки'''
        html = self.GetPage(self.GetBackLinksLink(domain))
        for indexRegexp in regexpsList:
            try:
                return int(re.findall(indexRegexp, html)[0].replace(',', ''))
            except Exception:
                pass
        return 0
        
    @classmethod
    def GetPosition(self, domain, keyword, regexp):
        '''Получаем позицию'''
        html = self.GetPage(self.GetPositionLink(keyword))
        urlsList = re.findall(regexp, html)
        urlsList = [urllib.unquote_plus(re.sub(r'<.*?>', '', url)).replace('&#8203;', '') for url in urlsList]
        counter = 1
        position = None
        extendedInfo = ''
        for url in urlsList:
            if url.find(domain) >= 0:
                if position == None:
                    position = counter
                if extendedInfo != '':
                    extendedInfo += '; '
                extendedInfo += '%d: %s' % (counter, url)
            counter += 1
        return position, extendedInfo
    
    
class Google(Engine):
    '''Гугл'''

    @classmethod
    def GetIndexLink(self, domain):
        '''Ссылка для проверки индекса'''
        url = 'http://www.google.com/search?hl=en&q=site:%s'
        return super(Google, self).GetLink(url, domain)
    
    @classmethod
    def GetIndex(self, domain):
        '''Получаем индекс'''
        regexpsList = [r'About ([0-9,]*) res', r'of about <b>([0-9,]*)</b>', r'<div>([0-9,]*) res']
        return super(Google, self).GetIndex(domain, regexpsList)
    
    @classmethod
    def GetPositionLink(self, keyword):
        '''Ссылка для проверки позиции'''
        url = 'http://www.google.com/search?hl=en&q=%s&num=100'
        return super(Google, self).GetLink(url, keyword)
    
    @classmethod
    def GetPosition(self, domain, keyword):
        '''Получаем позицию'''
        regexp = r'href="/url\?q=([^&]*)&'
        return super(Google, self).GetPosition(domain, keyword, regexp)


class Yahoo(Engine):
    '''Яху'''
    
    @classmethod
    def GetPositionLink(self, keyword):
        '''Ссылка для проверки позиции'''
        url = 'http://search.yahoo.com/search?n=100&p=%s'
        return super(Yahoo, self).GetLink(url, keyword)

    @classmethod
    def GetPosition(self, domain, keyword):
        '''Получаем позицию'''
        regexp = r'class=url>(.*?)</span>'
        return super(Yahoo, self).GetPosition(domain, keyword, regexp)


class Bing(Engine):
    '''Бинг'''
    
    @classmethod
    def GetPositionLink(self, keyword):
        '''Ссылка для проверки позиции'''
        url = 'http://www.bing.com/search?q=%s'
        return super(Bing, self).GetLink(url, keyword)

    @classmethod
    def GetPosition(self, domain, keyword):
        '''Получаем позицию'''
        regexp = r'class="sb_meta"><cite>(.*?)</cite>'
        return super(Bing, self).GetPosition(domain, keyword, regexp)


class Alexa(Engine):
    '''Алекса'''
    
    @classmethod
    def GetBackLinksLink(self, domain):
        '''Ссылка для проверки обратных ссылок'''
        url = 'http://www.alexa.com/siteinfo/%s'
        return super(Alexa, self).GetLink(url, domain)

    @classmethod
    def GetBackLinks(self, domain):
        '''Получаем обратные ссылки'''
        regexpsList = [r'/site/linksin.*?>([^<]*)<']
        return super(Alexa, self).GetBackLinks(domain, regexpsList)


class Majestic(Engine):
    '''Маджестик'''
    
    @classmethod
    def GetBackLinksLink(self, domain):
        '''Ссылка для проверки обратных ссылок'''
        url = 'http://www.majesticseo.com/reports/site-explorer/summary/%s/'
        return super(Majestic, self).GetLink(url, domain)

    @classmethod
    def GetBackLinks(self, domain):
        '''Получаем обратные ссылки'''
        regexpsList = [r'<p>\s*?External Backlinks\s*</p>\s*?<p.*?>\s*?<b>(.*?)</b>']
        return super(Majestic, self).GetBackLinks(domain, regexpsList)


if __name__ == '__main__':
    print(Google.GetIndex('sexgamesforxbox.net'))
    print(Google.GetPosition('sexgamesforxbox.net', 'sex games for xbox'))
    print(Yahoo.GetPosition('sexgamesforxbox.net', 'sex games for xbox'))
    print(Bing.GetPosition('sexgamesforxbox.net', 'sex games for xbox'))
    print(Alexa.GetBackLinks('myglutenfreediet.net'))
    print(Majestic.GetBackLinks('myglutenfreediet.net'))
