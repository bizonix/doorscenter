# coding=utf8
import os, sys, re, time, random, urllib, urllib2, pycurl, cStringIO, threading, Queue

requestUrl = 'http://www.google.com/search?q=%s&num=100&start=%d&hl=en&output=ie&filter=0&safe=off'
rxLinks = re.compile(r'<li class="g"><h3 class="r"><a.*?http://(.*?)&amp;')
proxiesUrl = 'http://awmproxy.com/socks_good_proxy.txt'
threadsCount = 250
pagesCount = 10

class Hrefer(object):
    '''Hrefer v.5.0'''
    
    def __init__(self):
        '''Инициализация'''
        self.workFolder = r'c:\Work\hrefer5'
        self.proxiesList = []
        
        self.queriesFileName = os.path.join(self.workFolder, 'queries3.txt')
        self.queriesList = []
        if os.path.exists(self.queriesFileName):
            self.queriesList = open(self.queriesFileName).read().splitlines()
        print('Queries: %d' % len(self.queriesList))
        
        self.filtersFileName = os.path.join(self.workFolder, 'filters.txt')
        self.filtersList = []
        if os.path.exists(self.filtersFileName):
            self.filtersList = open(self.filtersFileName).read().splitlines()
        print('Filters: %d' % len(self.filtersList))
        self.rxFilters = re.compile('(' + '|'.join([re.escape(item) for item in self.filtersList]) + ')')
        
        self.keywordsFileName = os.path.join(self.workFolder, 'keywords3.txt')
        self.keywordsList = []
        if os.path.exists(self.keywordsFileName):
            self.keywordsList = open(self.keywordsFileName).read().splitlines()
        print('Keywords: %d' % len(self.keywordsList))
        random.shuffle(self.keywordsList)
            
        self.linksFileName = None
        self.linksList = None
        self.queueIn = None
        self.queueOut = None
        self.running = False
    
    @classmethod
    def GetHost(self, url):
        '''Получаем хост по урлу'''
        host = url.strip().lower()
        if host.startswith('http://'):
            host = host[7:]
        if host.startswith('www.'):
            host = host[4:]
        host, _, _ = host.partition('/')
        return host
    
    def GetHtml(self, url):
        '''Читаем урл через случайный прокси и возвращаем текст'''
        attemptsCount = 2
        for _ in range(attemptsCount):
            try:
                buf = cStringIO.StringIO()
                curl = pycurl.Curl()
                curl.setopt(pycurl.HTTPHEADER, ["Accept:"])
                curl.setopt(pycurl.FOLLOWLOCATION, 1)
                curl.setopt(pycurl.MAXREDIRS, 5)
                curl.setopt(pycurl.CONNECTTIMEOUT, 3000)
                curl.setopt(pycurl.TIMEOUT, 3000)
                curl.setopt(pycurl.PROXY, random.choice(self.proxiesList).strip())
                curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
                curl.setopt(pycurl.URL, url)
                curl.setopt(pycurl.WRITEFUNCTION, buf.write)
                curl.setopt(pycurl.USERAGENT, 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
                curl.perform()
                return buf.getvalue()
            except Exception:
                pass
        return ''
    
    def UpdateProxy(self):
        '''Апдейтим прокси'''
        self.proxiesList = urllib2.urlopen(proxiesUrl).read().splitlines()
        print('Proxies: %d' % len(self.proxiesList))
        
    def FlushLinks(self):
        '''Извлекаем собранные ссылки из очереди ...'''
        print('Flushing links ...')
        while not self.queueOut.empty():
            url = self.queueOut.get()
            host = self.GetHost(url)
            if host not in self.hostsList:
                self.linksList.append(url)
                self.hostsList.append(host)
            self.queueOut.task_done()
        '''... и пишем их в файл'''
        open(self.linksFileName, 'w').write('\n'.join(self.linksList))
        print('Links flushed.')
        
    def Start(self, linksFileName):
        '''Запускаем парсинг'''
        '''Загружаем ссылки'''
        self.linksFileName = os.path.join(self.workFolder, linksFileName)
        self.linksList = []
        if os.path.exists(self.linksFileName): 
            self.linksList = open(self.linksFileName).read().splitlines()
        print('Links: %d' % len(self.linksList))
        self.hostsList = [self.GetHost(url) for url in self.linksList]
        
        '''Заполняем очереди'''
        self.queueIn = Queue.Queue()
        self.queueOut = Queue.Queue()
        for line1 in self.keywordsList:
            for line2 in self.queriesList:
                for page in range(pagesCount):
                    self.queueIn.put(('%s %s' % (line1, line2), page))
            if self.queueIn.qsize() > 100000:  # ограничиваем размер очереди
                break

        '''Запускаем потоки'''
        self.running = True
        self.UpdateProxy()
        HreferMonitor(self).start()
        for _ in range(threadsCount):
            HreferThread(self).start()
        self.queueIn.join()
        
        '''Конец'''
        self.running = False
        self.FlushLinks()
        print('Done')


class HreferMonitor(threading.Thread):
    '''Монитор хрефера'''
        
    def __init__(self, hrefer):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True
        self.hrefer = hrefer
        
    def run(self):
        print('Monitoring started.')
        lastActionTime1 = time.time()
        lastActionTime2 = time.time()
        lastActionTime3 = time.time()
        while self.hrefer.running:
            '''Каждые ... секунд выводим текущую информацию'''
            if time.time() - lastActionTime1 > 0:
                print('... %d/%d links, %d queries left' % (len(self.hrefer.linksList), self.hrefer.queueOut.qsize(), self.hrefer.queueIn.qsize()))
                lastActionTime1 = time.time()
            '''Каждые ... секунд сохраняем базу кейвордов'''
            if time.time() - lastActionTime2 > 120:
                self.hrefer.FlushLinks()
                lastActionTime2 = time.time()
            '''Каждые ... секунд апдейтим прокси'''
            if time.time() - lastActionTime3 > 180:
                self.hrefer.UpdateProxy()
                lastActionTime3 = time.time()
            time.sleep(1)
        print('Monitoring finished.')


class HreferThread(threading.Thread):
    '''Поток хрефера'''
        
    def __init__(self, hrefer):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True
        self.hrefer = hrefer
        
    def run(self):
        while not self.hrefer.queueIn.empty():
            query, page = self.hrefer.queueIn.get()
            try:
                html = self.hrefer.GetHtml(requestUrl % (urllib.quote_plus(query), page * 100))
                linksList = ['http://' + urllib.unquote_plus(url) for url in rxLinks.findall(html) if self.hrefer.rxFilters.search(urllib.unquote_plus(url))]
                for url in linksList:
                    self.hrefer.queueOut.put(url)
            except Exception:
                pass
            self.hrefer.queueIn.task_done()


hrefer = Hrefer()
hrefer.Start('links2.txt')
