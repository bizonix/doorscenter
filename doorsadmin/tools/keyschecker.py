# coding=utf8
import urllib, threading, Queue, random, re, pycurl, cStringIO, operator, datetime, time
random.seed()

proxyListAllUrl = 'http://proxylist.fineproxy.ru/all.txt'

googleCheckUrl = 'http://www.google.com/search?hl=en&q=%s&btnG=Google+Search'
googleSuccessStr = 'search tools</a>'
googleNoResultsStr1 = 'No results found for'
googleNoResultsStr2 = 'did not match any documents'
googleFailStr = 'unusual traffic from your computer'

class Proxy(object):
    '''Прокси. Умеет получать данные с заданного адреса. Заточен под работу с гуглом.'''
    
    def __init__(self, type, address, timeout = 10):
        self.type = type
        self.address = address
        self.timeout = timeout
        self.googleFails = 0
        self.googleAccess = True
        self.lastError = ''
    
    def __str__(self):
        return self.address
    
    def Read(self, url):
        '''Читаем урл и возвращаем текст'''
        attemptsCount = 2
        for _ in range(attemptsCount):
            try:
                buf = cStringIO.StringIO()
                curl = pycurl.Curl()
                curl.setopt(pycurl.HTTPHEADER, ["Accept:"])
                curl.setopt(pycurl.FOLLOWLOCATION, 1)
                curl.setopt(pycurl.MAXREDIRS, 5)
                curl.setopt(pycurl.CONNECTTIMEOUT, self.timeout)
                curl.setopt(pycurl.TIMEOUT, self.timeout)
                if self.type == 'http':
                    curl.setopt(pycurl.PROXY, self.address)
                curl.setopt(pycurl.URL, url)
                curl.setopt(pycurl.WRITEFUNCTION, buf.write)
                curl.setopt(pycurl.USERAGENT, 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
                curl.perform()
                return buf.getvalue()
            except Exception as error:
                self.lastError = str(error)
        return ''
    
    def GoogleRequest(self, query, maxFails = 5):
        '''Делаем запрос в гугл'''
        html = self.Read(googleCheckUrl % query)
        if (html != '') and (html.find(googleSuccessStr) < 0):
            self.googleFails += 1
        if (self.googleFails > maxFails) or (html.find(googleFailStr) >= 0):
            self.googleAccess = False
            #if html.find(googleFailStr) < 0:
            #    print('### Failed html: %s' % html)
        return html
        
class ProxyChecker(threading.Thread):
    '''Поточный чекер прокси'''

    def __init__(self, queueAll, queueChecked):
        threading.Thread.__init__(self)
        self.daemon = True
        self.queueAll = queueAll
        self.queueChecked = queueChecked

    def run(self):
        while not self.queueAll.empty():
            proxy = self.queueAll.get()
            proxy.GoogleRequest('"xxx"', 0)
            if proxy.googleAccess:
                self.queueChecked.put(proxy)
            #print('- %s: %s.' % (proxy, proxy.googleAccess))
            self.queueAll.task_done()

class KeywordChecker(threading.Thread):
    '''Поточный чекер кейвордов'''

    def __init__(self, queueIn, queueOut, proxyList):
        threading.Thread.__init__(self)
        self.daemon = True
        self.queueIn = queueIn
        self.queueOut = queueOut
        self.proxyList = proxyList
        self.rxList = [re.compile(r'About ([0-9,]*) res'), re.compile(r'of about <b>([0-9,]*)</b>'), re.compile(r'<div>([0-9,]*) res')]

    def run(self):
        while not self.queueIn.empty():
            keyword = self.queueIn.get()
            x = self.Check(keyword)
            print('- %s: %d' % (keyword, x))
            self.queueOut.put({keyword: x})
            self.queueIn.task_done()
    
    def Check(self, keyword):
        '''Делаем запрос'''
        query = urllib.quote_plus('"' + keyword + '"')
        attemptsCount = 200
        for _ in range(attemptsCount):
            proxy = random.choice(self.proxyList)
            if not proxy.googleAccess:
                continue
            #print('-- %s: %s' % (keyword, proxy))
            html = proxy.GoogleRequest(query)
            if not proxy.googleAccess:
                print('### Failed: %s' % proxy)
                continue
            if html == '':
                continue
            if (html.find(googleNoResultsStr1) >= 0) or (html.find(googleNoResultsStr2) >= 0):
                return 0
            for rx in self.rxList:
                try:
                    return int(rx.findall(html)[0].replace(',', ''))
                except Exception:
                    pass
            #print(html)
        return -1

class CheckerMonitor(threading.Thread):
    '''Монитор очередей'''
    
    def __init__(self, queue1, queue2):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue1 = queue1
        self.queue2 = queue2
        self.queue1InitialSize = self.queue1.qsize()
        
    def run(self):
        '''Каждые N секунд выводим текущую информацию'''
        lastActionTime = time.time()
        while not self.queue1.empty():
            if time.time() - lastActionTime > 5:
                print('%d/%d (%.2f%%) => %d.' % ((self.queue1InitialSize - self.queue1.qsize()), self.queue1InitialSize, (self.queue1InitialSize - self.queue1.qsize()) * 100.0 / self.queue1InitialSize, self.queue2.qsize()))
                lastActionTime = time.time()
            time.sleep(1)
        print('### Monitor finished.')


def CheckProxies():
    '''Проверка прокси'''
    print('=== Checking proxies ===')

    '''Инициализация'''
    dateTimeStart = datetime.datetime.now()
    proxyListAllStr = Proxy('none', '').Read(proxyListAllUrl).splitlines()
    print('Proxies total: %d.' % len(proxyListAllStr))

    '''Проверка'''
    threadsCount = 100
    queueProxyAll = Queue.Queue()
    queueProxyChecked = Queue.Queue()
    for item in proxyListAllStr:
        queueProxyAll.put(Proxy('http', item))
    CheckerMonitor(queueProxyAll, queueProxyChecked).start()
    for _ in range(threadsCount):
        ProxyChecker(queueProxyAll, queueProxyChecked).start()
    queueProxyAll.join()
    
    '''Обработка результатов'''
    proxyListChecked = []
    with open('proxies.txt', 'w') as fd:
        while not queueProxyChecked.empty():
            proxy = queueProxyChecked.get()
            fd.write(proxy.address + '\n')
            proxyListChecked.append(proxy)
            queueProxyChecked.task_done()
    print('Proxies checked: %d.' % len(proxyListChecked))

    '''Статистика'''
    timeDelta = (datetime.datetime.now() - dateTimeStart).seconds
    print('Checked %d proxies in %d sec. (%.2f sec./proxy)' % (len(proxyListAllStr), timeDelta, timeDelta * 1.0 / len(proxyListAllStr)))
    return proxyListChecked

def LoadProxies():
    '''Читаем прокси из файла'''
    print('=== Loading proxies ===')
    proxyListChecked = []
    for line in open('proxies.txt'):
        proxyListChecked.append(Proxy('http', line.strip()))
    print('Proxies checked: %d.' % len(proxyListChecked))
    return proxyListChecked

def CheckKeywords(keywordsFile):
    '''Проверка кейвородов'''
    print('=== Checking keywords ===')
    
    '''Читаем кейворды из базы'''
    keywordsDict = {}
    for line in open('keywords-db.txt'):
        if line.strip() == '':
            continue
        keyword, _, x = line.strip().rpartition(':')
        keywordsDict[keyword.strip()] = int(x.strip())

    '''Читаем новые кейворды'''
    keywordsTotal = 0
    keywordsList = []
    for line in open(keywordsFile):
        keyword = line.strip()
        if keyword == '':
            continue
        keywordsTotal += 1
        if keyword in keywordsDict:
            continue
        keywordsList.append(keyword)
    print('Keywords total: %d.' % keywordsTotal)
    keywordsListCount = len(keywordsList)
    print('Keywords to check: %d.' % keywordsListCount)
    
    '''Цикл по группам кейвордов'''
    chunkSize = 10000
    for n in range(keywordsListCount / chunkSize + 1):
        keywordsListChunk = keywordsList[n * chunkSize : (n + 1) * chunkSize]
        keywordsListChunkCount = len(keywordsListChunk)
        '''Помещаем группу в очередь'''
        queueKeywordsIn = Queue.Queue()
        queueKeywordsOut = Queue.Queue()
        for item in keywordsListChunk:
            queueKeywordsIn.put(item)
        '''Получаем свежие прокси'''
        proxyList = CheckProxies()
        #proxyList = LoadProxies()
        
        '''Проверка'''
        threadsCount = 100
        dateTimeStart = datetime.datetime.now()
        print('=== Checking keywords (part %d) ===' % (n + 1))
        CheckerMonitor(queueKeywordsIn, queueKeywordsOut).start()
        for _ in range(threadsCount):
            KeywordChecker(queueKeywordsIn, queueKeywordsOut, proxyList).start()
        queueKeywordsIn.join()
        '''Обработка результатов'''
        while not queueKeywordsOut.empty():
            keywordsDict.update(queueKeywordsOut.get())
            queueKeywordsOut.task_done()
        keywordsListSorted = sorted(keywordsDict.iteritems(), key=operator.itemgetter(1))
        '''Пишем кейворды в базу'''
        with open('keywords-db.txt', 'w') as fd:
            for item in keywordsListSorted:
                fd.write('%s: %d\n' % (item[0], item[1]))
        '''Статистика'''
        timeDelta = (datetime.datetime.now() - dateTimeStart).seconds
        print('Checked %d keywords in %d sec. (%.2f sec./keyword)' % (keywordsListChunkCount, timeDelta, timeDelta * 1.0 / keywordsListChunkCount))


def Test():
    '''Тест'''
    #proxy = Proxy('none', '')
    proxy = Proxy('http', '209.97.203.60:8080')
    print(proxy.GoogleRequest('"xxx"'))
    print(proxy.lastError)


CheckKeywords(r'C:\Users\sasch\workspace\doorscenter\src\doorsadmin\keywords\adult-new\[05]free personal.txt')
