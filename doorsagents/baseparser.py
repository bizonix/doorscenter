# coding=utf8
import os, urllib2, re, time, threading, Queue, kwk8

'''Настройки'''
urlOpenTimeout = 15
featuresList = '''/action=profile;u=
/forum.php?
/guest/index.php
/index.php?action=
/index.php?showforum=
/index.php?showtopic=
/index.php?showuser=
/index.php?topic=
/member.php?
/memberlist.php?
/newreply.php?
/posting.php?
/profile.php?
/reply.php?
/showthread.php?
/topic.php?
/viewthread.php?
/viewtopic.php?
/yabb.pl?'''.split('\n')

class Spider(threading.Thread):
    def __init__(self, queue, processedUrls, selectedDomains, selectedUrls):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue = queue
        self.processedUrls = processedUrls
        self.selectedDomains = selectedDomains
        self.selectedUrls = selectedUrls

    def run(self):
        global parseCancelled
        while not parseCancelled:
            '''Получаем ссылку из очереди'''
            url = self.queue.get() 
            '''Читаем страницу и извлекаем из нее ссылки'''
            urlsList = []
            try:
                #print('- getting %s' % url)
                fd = urllib2.urlopen(url, timeout=urlOpenTimeout)
                html = fd.read()
                urlsList = re.findall(r'href=[\'"](http[^\'"]*)[\'"]', html)
                fd.close()
            except Exception:
                pass
            '''Ссылки фильтруем на соответствие признакам'''
            urlsListFeatured = []
            for url in urlsList:
                for feature in featuresList:
                    if url.find(feature) >= 0:
                        urlsListFeatured.append(url)
                        break
            '''Обрабатываем полученные ссылки'''
            for url in urlsListFeatured:
                if url in self.processedUrls:
                    continue
                if not parseCancelled:
                    self.queue.put(url)
                domain = url.replace('http://', '').replace('www.', '')
                domain = domain[:domain.find('/')]
                if domain not in self.selectedDomains:
                    self.selectedUrls.append(url)
                    self.selectedDomains.append(domain)
                self.processedUrls.append(url)
            '''Завершение обработки ссылки'''
            self.queue.task_done()

class SpiderMonitor(threading.Thread):
    def __init__(self, queue, processedUrls, selectedDomains, selectedUrls, baseFileName, parseTimeout):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue = queue
        self.processedUrls = processedUrls
        self.selectedDomains = selectedDomains
        self.selectedUrls = selectedUrls
        self.baseFileName = baseFileName
        self.parseTimeout = parseTimeout

    def run(self):
        '''Каждые 5 секунд сохраняем базу в файл и выводим текущую информацию.
        По истечении тайматута завершаем выполнение потоков'''
        global parseCancelled
        startTime = time.time()
        lastActionTime = startTime 
        while not parseCancelled:
            '''Истек таймаут'''
            if time.time() - startTime > self.parseTimeout:
                parseCancelled = True
                while not self.queue.empty():
                    self.queue.get()
                    self.queue.task_done()
                print('Timed out')
            '''Пора сохранять базу'''
            if (time.time() - lastActionTime > 5) or parseCancelled:
                open(self.baseFileName, 'w').write('\n'.join(self.selectedUrls))
                lastActionTime = time.time()
                print('Base size: %d. Queue size: %d.' % (len(self.selectedDomains), self.queue.qsize()))
            time.sleep(1)

def Parse(xrumerFolder, startTopics, threadsCount, parseTimeout, baseNumber):
    '''Инициализация'''
    global parseCancelled
    xrumerLinksFolder = os.path.join(xrumerFolder, 'Links')
    baseFileName = os.path.join(xrumerLinksFolder, 'LinksList id%d.txt' % baseNumber)

    processedUrls = []
    selectedDomains = []
    selectedUrls = []
    parseCancelled = False
    queue = Queue.Queue()
    for startTopic in startTopics.split('\n'):
        queue.put(startTopic)
    
    '''Запускаем потоки'''
    for _ in range(threadsCount):
        Spider(queue, processedUrls, selectedDomains, selectedUrls).start()
    SpiderMonitor(queue, processedUrls, selectedDomains, selectedUrls, baseFileName, parseTimeout).start()
    
    '''Ждем окончания работы'''
    queue.join()
    
    '''Приводим базу к индексу'''
    kwk8.Kwk8Links(baseFileName).PostProcessing().Save(baseFileName)
    print('Done')

if __name__ == '__main__':
    startTopics = '''http://dlr-rus.ru/forum/viewtopic.php?t=92164'''
    xrumerFolder = r'c:\Work\xrumer708'
    Parse(xrumerFolder, startTopics, 100, 60, 1001)
