# coding=utf8
import pycurl, cStringIO, random, urllib, re

proxyUrls = ['174.127.67.236:554', '206.217.201.28:554', '206.217.201.30:554']
proxyUser = '218660178:dd7a0e1e'

class Engine(object):
    '''Предок используемых сайтов'''
    
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
            #curl.setopt(pycurl.URL, 'http://www.google.com/search?hl=en&q=jessica+simpson+shoes+cheap&num=100&btnG=Google+Search')
            curl.setopt(pycurl.WRITEFUNCTION, buf.write)
            curl.perform()
            return buf.getvalue()
        except Exception:
            return ''
    
class Google(Engine):
    '''Гугл'''

    @classmethod
    def GetIndexLink(self, domain):
        '''Ссылка для проверки индекса'''
        urlIndexSearch = 'http://www.google.com/search?hl=en&q=%s&btnG=Google+Search'
        return urlIndexSearch % urllib.quote_plus('site:' + domain.encode('cp1251'))
    
    def GetIndex(self, domain):
        '''Получаем индекс'''
        html = self.GetPage(self.GetIndexLink(domain))
        print(html)
        indexRegexpsList = [r'About ([0-9,]*) res', r'of about <b>([0-9,]*)</b>', r'<div>([0-9,]*) res']
        for indexRegexp in indexRegexpsList:
            try:
                return int(re.findall(indexRegexp, html)[0].replace(',', ''))
            except Exception:
                pass
        return 0
    
    @classmethod
    def GetPositionLink(self, keyword):
        '''Ссылка для проверки позиции'''
        urlPositionSearch = 'http://www.google.com/search?hl=en&q=%s&num=100&btnG=Google+Search'
        return urlPositionSearch % urllib.quote_plus(keyword.encode('cp1251'))
    
    def GetPosition(self, domain, keyword):
        '''Получаем позицию'''
        html = self.GetPage(self.GetPositionLink(keyword))
        urlsList = re.findall(r'href="/url\?q=([^&]*)&', html)
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
    
class Alexa(Engine):
    '''Алекса'''
    
    @classmethod
    def GetBackLinksLink(self, domain):
        '''Ссылка для проверки обратных ссылок'''
        url = 'http://www.alexa.com/siteinfo/%s'
        return url % domain.encode('cp1251')

    def GetBackLinks(self, domain):
        '''Получаем обратные ссылки'''
        html = self.GetPage(self.GetBackLinksLink(domain))
        backLinksRegexp = r'/site/linksin.*?>([^<]*)<'
        try:
            return int(re.findall(backLinksRegexp, html, re.M)[0].strip().replace(',', ''))
        except Exception:
            return 0
    
class Yahoo(Engine):
    '''Яху'''
    
    @classmethod
    def GetPositionLink(self, keyword):
        '''Ссылка для проверки позиции'''
        pass

    def GetPosition(self, domain, keyword):
        '''Получаем позицию'''
        pass
    
class Bing(Engine):
    '''Бинг'''
    
    @classmethod
    def GetPositionLink(self, keyword):
        '''Ссылка для проверки позиции'''
        pass

    def GetPosition(self, domain, keyword):
        '''Получаем позицию'''
        pass
    
if __name__ == '__main__':
    position, extendedInfo = Google.GetPosition('thejessicasimpsonshoes.com', 'jessica simpson shoes cheap')
    print(position, extendedInfo)
    #links = Alexa.GetBackLinks('thejessicasimpsonshoes.com')
    #print(links)
