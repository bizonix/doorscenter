# coding=utf8
import os, re, time, urllib2

class Hrefer(object):
    '''Hrefer v.6.0'''
    
    def __init__(self):
        '''Инициализация'''
        self.linksUrl = 'http://blogsearch.google.com/changes.xml?last=120'
        self.rxUrls = re.compile(r'url="([^"]*?)"')
        
        self.selfPath = os.path.dirname(__file__)
        self.linksFileName = os.path.join(self.selfPath, 'links.txt')
        self.filtersFileName = os.path.join(self.selfPath, 'filters.txt')

        self.linksList = []
        if os.path.exists(self.linksFileName): 
            self.linksList = open(self.linksFileName).read().splitlines()
        print('Links: %d' % len(self.linksList))
        self.hostsList = [self._GetHost(url) for url in self.linksList]

        self.filtersList = []
        if os.path.exists(self.filtersFileName):
            self.filtersList = open(self.filtersFileName).read().splitlines()
        print('Filters: %d' % len(self.filtersList))
        self.rxFilters = re.compile('(' + '|'.join([re.escape(item) for item in self.filtersList]) + ')')

    @classmethod
    def _GetHost(self, url):
        '''Получаем хост по урлу'''
        host = url.strip().lower()
        if host.startswith('http://'):
            host = host[7:]
        if host.startswith('www.'):
            host = host[4:]
        host, _, _ = host.partition('/')
        return host
    
    def Start(self):
        '''Запускаем парсинг'''
        while True:
            '''Получаем выдачу и парсим'''
            #xml = open(r'c:\temp\blogs.xml').read()
            xml = urllib2.urlopen(self.linksUrl).read()
            for url in self.rxUrls.findall(xml):
                if self.rxFilters.search(url):
                    host = self._GetHost(url)
                    if host not in self.hostsList:
                        self.linksList.append(url)
                        self.hostsList.append(host)
            
            '''Сохраняем ссылки в файл'''
            open(self.linksFileName, 'w').write('\n'.join(self.linksList))
            print('- %d links' % len(self.linksList))
            
            '''Ждем'''
            time.sleep(60)

if __name__ == '__main__':
    hrefer = Hrefer()
    hrefer.Start()
