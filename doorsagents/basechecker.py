# coding=utf8
import os, urllib2, time, threading, Queue, kwk8
from xml.etree.ElementTree import ElementTree

'''Настройки'''
urlOpenTimeout = 15

class Checker(threading.Thread):
    def __init__(self, queue, found, featuredText):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue = queue
        self.found = found
        self.featuredText = featuredText

    def run(self):
        '''Проверяем ссылки из очереди на наличие текста'''
        while True:
            url = self.queue.get() 
            try:
                #print('- getting %s' % url)
                fd = urllib2.urlopen(url, timeout=urlOpenTimeout)
                html = fd.read()
                if html.find(self.featuredText) >= 0:
                    self.found.put(url)
                fd.close()
            except Exception:
                pass
            self.queue.task_done()
        
class CheckerMonitor(threading.Thread):
    def __init__(self, queue, found):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue = queue
        self.found = found
        self.initialSize = self.queue.qsize()
        
    def run(self):
        '''Каждые 5 секунд выводим текущую информацию'''
        lastActionTime = time.time()
        while True:
            if time.time() - lastActionTime > 5:
                print('Found: %d/%d/%d.' % (self.found.qsize(), (self.initialSize - self.queue.qsize()), self.initialSize))
                lastActionTime = time.time()
            time.sleep(1)

def CheckBase(xrumerFolder, projectName, baseNumber, threadsCount):
    '''Параметры'''
    projectFile = os.path.join(xrumerFolder, 'Projects', projectName + '.xml')
    logFileTemplate = os.path.join(xrumerFolder, 'Logs', projectName, '%s id%d.txt' % ('%s', baseNumber))
    logSuccess = logFileTemplate % 'Success'
    logHalfSuccess = logFileTemplate % 'Halfsuccess'
    logFails = logFileTemplate % 'Others'
    xrumerLinksFolder = os.path.join(xrumerFolder, 'Links')
    baseFileName = os.path.join(xrumerLinksFolder, 'LinksList id%d.txt' % baseNumber)
    baseRFileName = os.path.join(xrumerLinksFolder, 'RLinksList id%d.txt' % baseNumber)
    baseZFileName = os.path.join(xrumerLinksFolder, 'ZLinksList id%d.txt' % baseNumber)

    '''Получаем фразу из проекта'''
    tree = ElementTree()
    tree.parse(projectFile)
    body = tree.getroot().findtext('SecondarySection/PostText')
    while body.find('[') >= 0:
        pos1 = body.find('[')
        pos2 = body.find(']', pos1)
        body = body[:pos1].strip() + '\n' + body[pos2+1:].strip()
    body = body.replace('#file_links', '').strip()
    featuredText = body.split('\n')[0]
    print('Looking for "%s"' % featuredText)
    
    '''Добавляем ссылки из логов в очередь'''
    queue = Queue.Queue()
    found = Queue.Queue()
    for fileName in [logSuccess, logHalfSuccess, logFails]:
        if os.path.exists(fileName):
            for line in open(fileName):
                url, _, _ = line.strip().partition(' ')
                queue.put(url)
    
    '''Запускаем потоки проверки и ждем окончания'''
    for _ in range(threadsCount):
        Checker(queue, found, featuredText).start()
    CheckerMonitor(queue, found).start()
    time.sleep(5)
    queue.join()
    
    '''Записываем найденные домены во временный файл'''
    print('Saving links found ...')
    tempFileName = os.path.join(xrumerLinksFolder, 'TLinksList id%d.txt' % baseNumber)
    with open(tempFileName, 'w') as fd:
        try:
            while True:
                fd.write(found.get_nowait() + '\n')
                found.task_done()
        except Exception:
            pass
    
    '''Фильтруем базы по файлу с найденными доменами'''
    print('Filtering bases ...')
    for fileName in [baseFileName, baseRFileName, baseZFileName]:
        if os.path.exists(fileName):
            kwk8.Kwk8Links(fileName).SelectByFile(tempFileName).Save(fileName)
    
    '''Удаляем временный файл'''
    try:
        os.remove(tempFileName)
    except Exception:
        pass
    print('Done.')
    
if __name__ == '__main__':
    xrumerFolder = r'c:\Work\xrumer708'
    CheckBase(xrumerFolder, 'ProjectS8530', 995, 100)
