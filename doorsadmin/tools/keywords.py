# coding=utf8
import urllib, threading, Queue, random, re, operator, datetime, googleproxy

keywordsDatabaseFile = 'keywords-db.txt'

googleResultsStrList = [r'About ([0-9,]*) res', r'of about <b>([0-9,]*)</b>', r'<div>([0-9,]*) res']
googleNoResultsStr1 = 'No results found for'
googleNoResultsStr2 = 'did not match any documents'

class KeywordsDatabase(object):
    '''База кейвордов'''
    
    def __init__(self):
        '''Инициализация'''
        self.keywordsDict = {}
        for line in open(keywordsDatabaseFile):
            if line.strip() == '':
                continue
            keyword, _, data = line.strip().rpartition(':')
            self.keywordsDict[keyword.strip()] = data.strip()
            
    def Has(self, keyword):
        '''Есть ли кейворд в базе'''
        return keyword in self.keywordsDict
    
    def Add(self, keyword, data):
        '''Добавляем кейворд в базу'''
        self.keywordsDict[keyword] = data
        
    def Flush(self):
        '''Сохраняем базу в отсортированном виде'''
        with open(keywordsDatabaseFile, 'w') as fd:
            keywordsListSorted = sorted(self.keywordsDict.iteritems(), key=operator.itemgetter(1))
            for item in keywordsListSorted:
                fd.write('%s: %d\n' % (item[0], item[1]))

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

def CheckKeywordsList(keywordsList):
    '''Проверка кейвородов из списка'''
    print('Checking keywords ...')
    keywordsDatabase = KeywordsDatabase()
    keywordsListNew = [item for item in keywordsList if not keywordsDatabase.Has(item)]
    print('Keywords to check: %d/%d.' % (len(keywordsListNew), len(keywordsList)))

    '''Цикл по группам кейвордов'''
    chunkSize = 10000
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
        googleproxy.CommonCheckerMonitor(queueKeywordsIn, queueKeywordsOut).start()
        for _ in range(threadsCount):
            KeywordsChecker(queueKeywordsIn, queueKeywordsOut, proxyList).start()
        queueKeywordsIn.join()
        
        '''Передаем результаты в базу данных'''
        while not queueKeywordsOut.empty():
            d = queueKeywordsOut.get()
            keywordsDatabase.Add(d.key, d.value)
            queueKeywordsOut.task_done()
        keywordsDatabase.Flush()

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

CheckKeywordsFile(r'C:\Users\sasch\workspace\doorscenter\src\doorsadmin\keywords\adult-new\[05]free personal.txt')
