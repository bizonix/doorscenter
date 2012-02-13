# coding=utf8
import os, re, glob, codecs, math, random, urllib, operator, datetime, time, threading, Queue, googleproxy

databaseFileName = 'keywords-data.txt'

googleResultsStrList = [r'About ([0-9,]*) res', r'of about <b>([0-9,]*)</b>', r'<div>([0-9,]*) res']
googleNoResultsStr1 = 'No results found for'
googleNoResultsStr2 = 'did not match any documents'

class KeywordsDatabaseGlobal(object):
    '''Класс для работы с несколькими базами кейвордов'''
    
    def __init__(self, folder):
        '''Инициализация'''
        self.folder = folder
        self.keywordsDataDict = {}
    
    def UpdateData(self):
        '''Проверка кейвородов в гугле'''
        self.keywordsDataDict = {}
        '''Формируем глобальную базу'''
        for path, _, _ in os.walk(self.folder):
            if path == self.folder:
                continue
            database = KeywordsDatabase(path)
            database.LoadData()
            self.keywordsDataDict.update(database.keywordsDataDict)
        print('The global keywords database size: %d.' % len(self.keywordsDataDict))
        '''Апдейтим каждую базу и снова апдейтим глобальную'''
        for path, _, _ in os.walk(self.folder):
            if path == self.folder:
                continue
            print('\nProcessing "%s" ...' % path)
            database = KeywordsDatabase(path)
            database.UpdateData(self)
            self.keywordsDataDict.update(database.keywordsDataDict)
        print('The global keywords database size: %d.' % len(self.keywordsDataDict))
    
class KeywordsDatabase(object):
    '''База кейвордов'''
    
    def __init__(self, folder, encoding='utf-8'):
        '''Инициализация'''
        self.folder = folder
        self.encoding = encoding
        self.databaseFile = os.path.join(self.folder, databaseFileName)
        self.keywordsFileMask = os.path.join(self.folder, r'[*.txt')
        self.keywordsDataDict = {}
        self.keywordsListCheck = []
        self.queueKeywordsIn = None
        self.queueKeywordsOut = None
    
    def Count(self):
        '''Считаем количество кейвордов'''
        n = 0
        for fileName in glob.glob(self.keywordsFileMask):
            for line in open(fileName, 'r'):
                if line.strip() != '':
                    n += 1
        return n

    def LoadData(self):
        '''Читаем данные по кейвордам'''
        self.keywordsDataDict = {}
        if os.path.exists(self.databaseFile):
            for line in open(self.databaseFile):
                if line.strip() == '':
                    continue
                try:
                    keyword, _, data = line.strip().rpartition(':')
                    keyword = keyword.strip()
                    data = int(data.strip())
                    if data != -1:
                        self.keywordsDataDict[keyword] = data
                    if (data == -1) and (keyword not in self.keywordsListCheck):
                        self.keywordsListCheck.append(keyword)
                except Exception as error:
                    #print('### Error: %s' % error)
                    pass
    
    def FlushData(self):
        '''Забираем результаты из очереди ...'''
        if self.queueKeywordsOut != None:
            while not self.queueKeywordsOut.empty():
                d = self.queueKeywordsOut.get()
                self.keywordsDataDict.update(d)
                self.queueKeywordsOut.task_done()
        '''... и сохраняем базу в отсортированном виде'''
        with open(self.databaseFile, 'w') as fd:
            keywordsListSorted = sorted(self.keywordsDataDict.iteritems(), key=operator.itemgetter(1))
            for item in keywordsListSorted:
                fd.write('%s: %d\n' % (item[0], item[1]))
        print('Keywords database flushed (%d items).' % len(self.keywordsDataDict))
        
    def UpdateData(self, globalDatabase = None):
        global monitorCancelled
        '''Проверка кейвородов в гугле'''
        print('Checking keywords ...')
        
        '''Читаем кейворды и данные по ним'''
        self.keywordsListCheck = []
        self.LoadData()
        for fileName in glob.glob(self.keywordsFileMask):
            for keyword in open(fileName):
                keyword = keyword.strip()
                if keyword == '':
                    continue
                if keyword not in self.keywordsDataDict:
                    self.keywordsListCheck.append(keyword)
        print('Keywords database size: %d.' % len(self.keywordsDataDict))
        print('Keywords to check: %d.' % len(self.keywordsListCheck))
        
        '''Делаем апдейт из глобальной базы'''
        if globalDatabase != None:
            print('Updating from the global database ...')
            for keyword in self.keywordsListCheck:
                if keyword in globalDatabase.keywordsDataDict:
                    self.keywordsDataDict[keyword] = globalDatabase.keywordsDataDict[keyword]
                    self.keywordsListCheck.remove(keyword)
            self.FlushData()
            print('Keywords database size: %d.' % len(self.keywordsDataDict))
            print('Keywords to check: %d.' % len(self.keywordsListCheck))
    
        if len(self.keywordsListCheck) <= 20:
            return
        
        proxyList = googleproxy.GoogleProxiesList()
        proxyList.Update()
    
        '''Помещаем группу в очередь'''
        dateTimeStart = datetime.datetime.now()
        self.queueKeywordsIn = Queue.Queue()
        self.queueKeywordsOut = Queue.Queue()
        for item in self.keywordsListCheck:
            self.queueKeywordsIn.put(item)
        
        '''Проверка'''
        threadsCount = 100
        monitorCancelled = False
        KeywordsCheckerMonitor(self.queueKeywordsIn, self.queueKeywordsOut, self, proxyList, len(self.keywordsListCheck)).start()
        for _ in range(threadsCount):
            KeywordsChecker(self.queueKeywordsIn, self.queueKeywordsOut, proxyList).start()
        self.queueKeywordsIn.join()
        monitorCancelled = True
        self.FlushData()
        
        '''Статистика'''
        timeDelta = (datetime.datetime.now() - dateTimeStart).seconds
        print('Checked %d keywords in %d sec. (%.2f sec./keyword)' % (len(self.keywordsListCheck), timeDelta, timeDelta * 1.0 / len(self.keywordsListCheck)))
    
    def _GetKeywordCompetition(self, keyword):
        '''Получаем конкуренцию по кейворду'''
        if keyword in self.keywordsDataDict:
            return self.keywordsDataDict[keyword]
        else:
            return 99999999999
        
    def _GetFilePercent(self, fileName):
        '''Получаем цифру из названия файла'''
        try:
            return int(re.match(r'^\[(.*?)\].*', fileName).group(1))
        except Exception:
            return 0
    
    def SelectKeywords(self, keywordsCountTotal = 100, maxCompetition = -1):
        '''Создание списка кеев для доров по Бабулеру.
        Для каждого дора из каждого файла в папке берется заданный процент кеев.'''
        if maxCompetition >= 0:
            self.LoadData()
        resultList = []
        percentsTotal = 0
        for fileName in glob.glob(self.keywordsFileMask):
            percentsTotal += self._GetFilePercent(fileName)
        for fileName in glob.glob(self.keywordsFileMask):
            percents = self._GetFilePercent(fileName)
            keywordsList = [line.strip() for line in codecs.open(fileName, 'r', self.encoding, 'ignore').readlines()]
            if maxCompetition >= 0:
                keywordsList = [keyword for keyword in keywordsList if self._GetKeywordCompetition(keyword) <= maxCompetition]
            keywordsCount = int(min(len(keywordsList), math.floor(keywordsCountTotal * percents / percentsTotal * random.randint(80, 120) / 100))) 
            if keywordsCount > 0:
                random.shuffle(keywordsList)
                resultList.extend(keywordsList[0:keywordsCount])
            keywordsCountTotal -= keywordsCount
            percentsTotal -= percents
        '''Перемешиваем готовый список'''
        random.shuffle(resultList)
        return resultList

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
            data = self.GetData(keyword)
            print('- %s: %d' % (keyword, data))
            self.queueOut.put({keyword: data})
            self.queueIn.task_done()
    
    def GetData(self, keyword):
        '''Делаем запрос в гугл'''
        query = urllib.quote_plus('"' + keyword + '"')
        attemptsCount = 200
        for _ in range(attemptsCount):
            proxy = self.proxyList.GetRandom()
            if not proxy.googleAccess:
                continue
            #print('-- %s: %s' % (keyword, proxy))
            html = proxy.Request(query)
            if not proxy.googleAccess:
                print('### Proxy failed: %s' % proxy)
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
    
    def __init__(self, queue1, queue2, keywordsDatabase, proxyList, keywordsListCount):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue1 = queue1
        self.queue2 = queue2
        self.proxyList = proxyList
        self.keywordsDatabase = keywordsDatabase
        self.keywordsListCount = keywordsListCount
        self.queue1InitialSize = self.queue1.qsize()
        
    def run(self):
        global monitorCancelled
        print('Monitoring started.')
        lastActionTime1 = time.time()
        lastActionTime2 = time.time()
        lastActionTime3 = time.time()
        while not monitorCancelled:
            '''Каждые N секунд выводим текущую информацию'''
            if time.time() - lastActionTime1 > 5:
                offset = self.queue1InitialSize - self.queue1.qsize()
                print('... %d/%d (%.2f%%).' % (offset, self.keywordsListCount, offset * 100.0 / self.keywordsListCount))
                lastActionTime1 = time.time()
            '''Каждые M секунд сохраняем базу кейвордов'''
            if time.time() - lastActionTime2 > 60:
                self.keywordsDatabase.FlushData()
                lastActionTime2 = time.time()
            '''Каждые X секунд апдейтим прокси'''
            if time.time() - lastActionTime3 > 60 * 3:
                self.proxyList.Update()
                lastActionTime3 = time.time()
            time.sleep(1)
        self.keywordsDatabase.FlushData()
        print('Monitoring finished.')

if __name__ == '__main__':
    db = KeywordsDatabaseGlobal(r'C:\Work\keys\en-dating')
    db.UpdateData()
    '''keywordsDatabase = KeywordsDatabase(r'D:\Miscellaneous\Lodger6\keys9\4')
    print(keywordsDatabase.Count())
    keywordsDatabase.UpdateData()'''
