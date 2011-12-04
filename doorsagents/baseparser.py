# coding=utf8
import urllib, re, time, threading, Queue

'''Параметры'''
baseFileName = 'LinksList id1.txt'
maxThreadsCount = 100
startTopic = 'http://studentcafeonline.com/viewtopic.php?f=3&t=107417'
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
    def __init__(self, url, queue1, queue2):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.url = url
        self.queue1 = queue1
        self.queue2 = queue2
        self.queue2.put('1')
        self.queue2.task_done()
    
    def run(self):
        global processedUrls, selectedDomains, selectedUrls
        '''Читаем страницу и извлекаем из нее ссылки'''
        urlsList = []
        try:
            print('Getting %s...' % self.url)
            fd = urllib.urlopen(self.url)
            html = fd.read()
            urlsList = re.findall(r'href=[\'"](http[^\'"]*)[\'"]', html)
            fd.close()
        except Exception as error:
            print('Error: %s' % error)
        '''Ссылки фильтруем на соответствие признакам'''
        urlsListFeatured = []
        for url in urlsList:
            for feature in featuresList:
                if url.find(feature) >= 0:
                    urlsListFeatured.append(url)
                    break
        '''Обрабатываем полученные ссылки'''
        for url in urlsListFeatured:
            if url in processedUrls:
                continue
            self.queue1.put(url)
            self.queue1.task_done()
            domain = url.replace('http://', '').replace('www.', '')
            domain = domain[:domain.find('/')]
            if domain not in selectedDomains:
                selectedUrls.append(url)
                selectedDomains.append(domain)
            processedUrls.append(url)
        '''Завершение работы потока'''
        self.queue2.get()
        print('Base size: %d. Queue size: %d. Threads count: %d.' % (len(selectedDomains), self.queue1.qsize(), self.queue2.qsize()))

'''Инициализация'''
processedUrls = []
selectedDomains = []
selectedUrls = []
queuedUrls = Queue.Queue()
queuedUrls.put(startTopic)
runningThreads = Queue.Queue()

'''Бесконечный цикл обработки'''
lastSavedTime = 0
while True:
    '''Соблюдаем максимальное число потоков'''
    while runningThreads.qsize() > maxThreadsCount:
        time.sleep(1)
    '''Запускаем новый поток'''
    Spider(queuedUrls.get(), queuedUrls, runningThreads).start()
    '''Каждые 10 секунд сохраняем базу в файл'''
    if time.time() - lastSavedTime > 10:
        open(baseFileName, 'w').write('\n'.join(selectedUrls))
        lastSavedTime = time.time()
        print('*** Base saved ***')
