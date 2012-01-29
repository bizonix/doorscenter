# coding=utf8
import os, re, glob, urllib, random, operator, datetime, time, threading, Queue, googleproxy

keywordsDatabaseFile = 'keywords-db.txt'

googleResultsStrList = [r'About ([0-9,]*) res', r'of about <b>([0-9,]*)</b>', r'<div>([0-9,]*) res']
googleNoResultsStr1 = 'No results found for'
googleNoResultsStr2 = 'did not match any documents'

class KeywordsDatabase(object):
    '''База кейвордов'''
    
    def __init__(self):
        '''Инициализация'''
        self.keywordsDict = {}
        self.keywordsCheckList = []
        if os.path.exists(keywordsDatabaseFile):
            for line in open(keywordsDatabaseFile):
                if line.strip() == '':
                    continue
                keyword, _, data = line.strip().rpartition(':')
                keyword = keyword.strip()
                data = int(data.strip())
                self.keywordsDict[keyword] = data
                if data == -1:
                    self.keywordsCheckList.append(keyword)
        print('Keywords database size: %d, to check: %d.' % (len(self.keywordsDict), len(self.keywordsCheckList)))
            
    def Has(self, keyword):
        '''Есть ли кейворд в базе'''
        return keyword in self.keywordsDict
    
    def Add(self, keyword, data):
        '''Добавляем данные по кейворду в базу'''
        self.keywordsDict[keyword] = data
        
    def GetData(self, keyword, default = None):
        '''Получаем данные по кейворду'''
        if self.Has(keyword):
            return self.keywordsDict[keyword]
        else:
            return default
        
    def Flush(self):
        '''Сохраняем базу в отсортированном виде'''
        with open(keywordsDatabaseFile, 'w') as fd:
            keywordsListSorted = sorted(self.keywordsDict.iteritems(), key=operator.itemgetter(1))
            for item in keywordsListSorted:
                fd.write('%s: %d\n' % (item[0], item[1]))
        print('Keywords database flushed (%d items).' % len(self.keywordsDict))
        
    def FlushQueue(self, queue):
        '''Забираем результаты из очереди и сохраняем базу'''
        while not queue.empty():
            d = queue.get()
            self.Add(d.keys()[0], d.values()[0])
            queue.task_done()
        self.Flush()
        
    def FilterKeywordsList(self, keywordsList, maxData):
        '''Отбираем ко конкуренции'''
        return [item for item in keywordsList if self.GetData(item, maxData + 1) <= maxData]

class KeywordsChecker(threading.Thread):
    '''Поточный чекер кейвордов в гугле'''

    def __init__(self, queueIn, queueOut, proxyList):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True
        self.queueIn = queueIn
        self.queueOut = queueOut
        self.proxyList = proxyList
        self.rxList = [re.compile(item) for item in googleResultsStrList]

    def run(self):
        '''Обработка очередей'''
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
            html = proxy.Request(query)
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

class KeywordsCheckerMonitor(threading.Thread):
    '''Монитор чекера прокси'''
    
    def __init__(self, queue1, queue2, keywordsDatabase, keywordsListOffset, keywordsListCount):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue1 = queue1
        self.queue2 = queue2
        self.keywordsDatabase = keywordsDatabase
        self.keywordsListOffset = keywordsListOffset
        self.keywordsListCount = keywordsListCount
        self.queue1InitialSize = self.queue1.qsize()
        
    def run(self):
        print('Monitoring started.')
        lastActionTime1 = time.time()
        lastActionTime2 = time.time()
        while not self.queue1.empty():
            '''Каждые N секунд выводим текущую информацию'''
            if time.time() - lastActionTime1 > 5:
                currentOffset = self.keywordsListOffset + self.queue1InitialSize - self.queue1.qsize()
                print('... %d/%d (%.2f%%).' % (currentOffset, self.keywordsListCount, currentOffset * 100.0 / self.keywordsListCount))
                lastActionTime1 = time.time()
            '''Каждые M секунд сохраняем базу кейвордов'''
            if time.time() - lastActionTime2 > 60:
                self.keywordsDatabase.FlushQueue(self.queue2)
                lastActionTime2 = time.time()
            time.sleep(1)
        self.keywordsDatabase.FlushQueue(self.queue2)
        print('Monitoring finished.')

def CheckKeywordsList(keywordsList):
    '''Проверка кейвородов из списка'''
    print('Checking keywords ...')
    keywordsList = list(set(keywordsList))
    keywordsDatabase = KeywordsDatabase()
    keywordsListNew = [item for item in keywordsList if not keywordsDatabase.Has(item)]
    print('Keywords to check: %d/%d/%d.' % (len(keywordsDatabase.keywordsCheckList), len(keywordsListNew), len(keywordsList)))
    keywordsListNew.extend(keywordsDatabase.keywordsCheckList)

    '''Цикл по группам кейвордов'''
    chunkSize = 5000
    chunksCount = (len(keywordsListNew) - 1) / chunkSize + 1
    for n in range(chunksCount):
        '''Получаем свежие прокси'''
        proxyList = googleproxy.ParseProxies()

        '''Помещаем группу в очередь'''
        dateTimeStart = datetime.datetime.now()
        print('Checking keywords (part %d/%d) ...' % (n + 1, chunksCount))
        keywordsListChunk = keywordsListNew[n * chunkSize : (n + 1) * chunkSize]
        keywordsListChunkCount = len(keywordsListChunk)
        queueKeywordsIn = Queue.Queue()
        queueKeywordsOut = Queue.Queue()
        for item in keywordsListChunk:
            queueKeywordsIn.put(item)
        
        '''Проверка'''
        threadsCount = 100
        KeywordsCheckerMonitor(queueKeywordsIn, queueKeywordsOut, keywordsDatabase, n * chunkSize, len(keywordsListNew)).start()
        for _ in range(threadsCount):
            KeywordsChecker(queueKeywordsIn, queueKeywordsOut, proxyList).start()
        queueKeywordsIn.join()
        keywordsDatabase.FlushQueue(queueKeywordsOut)
        
        '''Статистика'''
        timeDelta = (datetime.datetime.now() - dateTimeStart).seconds
        print('Checked %d keywords in %d sec. (%.2f sec./keyword)' % (keywordsListChunkCount, timeDelta, timeDelta * 1.0 / keywordsListChunkCount))

def CheckKeywordsFile(keywordsFile):
    '''Проверка кейвородов из файла'''
    keywordsList = []
    for line in open(keywordsFile):
        if line.strip() != '':
            keywordsList.append(line.strip())
    CheckKeywordsList(keywordsList)

def CheckKeywordsFolder(keywordsFolder):
    '''Проверка кейвородов из папки'''
    keywordsList = []
    for fileName in glob.glob(os.path.join(keywordsFolder, '*.txt')):
        for line in open(fileName):
            if line.strip() != '':
                keywordsList.append(line.strip())
    CheckKeywordsList(keywordsList)

CheckKeywordsFolder(r'C:\Users\sasch\workspace\doorscenter\src\doorsadmin\keywords\*')
