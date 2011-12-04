# coding=utf8
import urllib, re, time, threading, Queue

'''Параметры'''
threadsCount = 100
baseFileName = 'LinksList id1.txt'
startTopicsList = '''http://studentcafeonline.com/viewtopic.php?f=3&t=81331
http://studentcafeonline.com/viewtopic.php?f=3&t=108702
http://studentcafeonline.com/viewtopic.php?f=3&t=108701'''.split('\n')
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

class BaseSpider(threading.Thread):
    def __init__(self, queue):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.queue = queue
    
    def run(self):
        global processedUrls, selectedDomains, selectedUrls
        while True:
            '''Получаем ссылку из очереди'''
            url = self.queue.get() 
            '''Читаем страницу и извлекаем из нее ссылки'''
            urlsList = []
            try:
                print('- getting %s' % url)
                fd = urllib.urlopen(url)
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
                if url in processedUrls:
                    continue
                self.queue.put(url)
                domain = url.replace('http://', '').replace('www.', '')
                domain = domain[:domain.find('/')]
                if domain not in selectedDomains:
                    selectedUrls.append(url)
                    selectedDomains.append(domain)
                processedUrls.append(url)
            '''Завершение обработки ссылки'''
            self.queue.task_done()

class BaseMonitor(threading.Thread):
    def __init__(self, queue):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.queue = queue
    
    def run(self):
        '''Каждые 10 секунд сохраняем базу в файл и выводим текущую информацию'''
        lastActionTime = time.time()
        while True:
            if time.time() - lastActionTime > 5:
                open(baseFileName, 'w').write('\n'.join(selectedUrls))
                lastActionTime = time.time()
                print('Base size: %d. Queue size: %d.' % (len(selectedDomains), self.queue.qsize()))
            time.sleep(1)

'''Инициализация'''
processedUrls = []
selectedDomains = []
selectedUrls = []
queue = Queue.Queue()
for startTopic in startTopicsList:
    queue.put(startTopic)

'''Запускаем потоки'''
for _ in range(threadsCount):
    thread = BaseSpider(queue)
    thread.daemon = True
    thread.start()
thread = BaseMonitor(queue)
thread.daemon = True
thread.start()

'''Ждем окончания работы'''
queue.join()
