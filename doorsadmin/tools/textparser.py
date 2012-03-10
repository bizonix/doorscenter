# coding=utf8

import os, re, random, cookielib, tempfile, datetime, time, urllib, urllib2, threading, Queue, HTMLParser

'''
1. Парсинг ссылок из выдачи.
2. Парсинг текста с сайтов из выдачи.
3. Чистка текста в файлах.
'''

class LinksParser(object):
    '''Парсер ссылок с выдачи'''
    
    def __init__(self):
        '''Инициализация'''
        self.linksList = []
        self.pause = 5  # время между запросами в секундах
        self.rxLinks = re.compile(r'<h3 class=\"r\"><a href=\"/url\?q=(.+?)&amp;', re.S)
        self.userAgentsList = '''Opera/10.00 (Windows NT 5.1; U; ru) Presto/2.2.0
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.2; OfficeLiveConnector.1.3; OfficeLivePatch.0.0; .NET CLR 3.5.30729; .NET CLR 3.0.30618)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 1.1.4322; InfoPath.1)
Opera/9.62 (Windows NT 5.1; U; ru) Presto/2.1.1
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; GTB5; MRSPUTNIK 2, 0, 1, 31 SW; MRA 5.2 (build 02415); .NET CLR 1.1.4322; InfoPath.2; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)
Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 1.1.4322)
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FunWebProducts; (R1 1.5); .NET CLR 1.1.4322)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; FunWebProducts; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.1)
Mozilla/5.0 (Windows; U; Windows NT 5.1; pl; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1)
Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11
Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.8.0.6) Gecko/20060728 Firefox/1.5.0.6
Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)
Opera/9.25 (Windows NT 5.1; U; pl)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; AT&amp;T CSM6.0; .NET CLR 1.1.4322)
Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.7) Gecko/20060909 Firefox/1.5.0.7
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FDM)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.04506.30; InfoPath.2)
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; .NET CLR 2.0.50727)
Opera/9.20 (Windows NT 5.1; U; ru)
Opera/9.23 (Windows NT 5.1; U; ru)
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FileDownloader; .NET CLR 1.0.3705; .NET CLR 1.1.4322; InfoPath.1; FileDownloader; Media Center PC 4.0; .NET CLR 2.0.50727; MEGAUPLOAD 2.0)
Opera/9.21 (Windows NT 5.0; U; ru)
Opera/9.25 (Windows NT 5.1; U; bg)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; PeoplePal 3.0)
Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1); afcid=Wadf57d6951da76af4c6f0b08181c298d
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; MEGAUPLOAD 2.0)
Opera/8.54 (Windows NT 5.1; U; ru)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; YComp 5.0.0.0; .NET CLR 1.0.3705; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648)SAMSUNG-SGH-P910/1.0 SHP/VPP/R5 NetFront/3.3 SMM-MMS/1.2.0 profile/MIDP-2.0 configuration/CLDC-1.1
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; ADVPLUGIN|K115|165|S548873517|dial; 666XXX040507; .NET CLR 2.0.50727)'''.split('\n')
        self.cookieJar = cookielib.LWPCookieJar(os.path.join(tempfile.gettempdir(), '.google-cookie'))
    
    def Process(self, keywordsList, fileName, language = 'en'):
        '''Парсинг ссылок'''
        print('Parsing links ...')
        dateTimeStart = datetime.datetime.now()
        self.linksList = []
        for keyword in keywordsList:
            try:
                keyword = keyword.strip()
                print('- %s' % keyword)
                '''Делаем запрос'''
                url = 'http://www.google.com/search?as_q=%s&tbs=qdr:z&num=100&hl=%s&output=ie&filter=0' % (urllib.quote_plus(keyword), language)
                request = urllib2.Request(url)
                request.add_header('User-Agent', random.choice(self.userAgentsList))
                self.cookieJar.add_cookie_header(request)
                response = urllib2.urlopen(request)
                html = response.read()
                response.close()
                '''Парсим ответ'''
                self.linksList.extend(self.rxLinks.findall(html))
            except Exception:
                pass
        open(fileName, 'w').write('\n'.join(self.linksList))
        print('Parsed %d links in %d sec.' % (len(self.linksList), (datetime.datetime.now() - dateTimeStart).seconds))
        return self.linksList


class TextsDownloader(object):
    '''Скачивает текст по списку ссылок'''
    
    def __init__(self):
        '''Инициализация'''
        self.queueLinks = Queue.Queue()
        self.queueTexts = Queue.Queue()
        self.monitoring = False
        self.texts = ''
        self.fileName = None
    
    def Flush(self):
        '''Сохраняем текст'''
        print('Flushing texts ...')
        while not self.queueTexts.empty():
            self.texts += self.queueTexts.get()
            self.queueTexts.task_done()
        open(self.fileName, 'w').write(self.texts)
    
    def Process(self, linksList, fileName):
        '''Скачиваем текст'''
        print('Downloading texts ...')
        threadsCount = 100
        self.queueLinks = Queue.Queue()
        self.queueTexts = Queue.Queue()
        self.texts = ''
        self.fileName = fileName
        
        for link in linksList:
            link = link.strip()
            if link.startswith('http://'):
                self.queueLinks.put(link)
        self.monitoring = True
        TextsDownloaderMonitor(self).start()
        for _ in range(threadsCount):
            TextsDownloaderThreaded(self).start()
        self.queueLinks.join()
        self.monitoring = False
        self.Flush()
        print('Done.')
        return self.texts
        

class TextsDownloaderThreaded(threading.Thread):
    '''Поток скачивания текста'''
    
    def __init__(self, parent):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True
        self.parent = parent
        self.cleaner = TextsCleaner(True)

    def run(self):
        '''Обработка очередей'''
        while not self.parent.queueLinks.empty():
            link = self.parent.queueLinks.get()
            text = self.Process(link)
            text = self.cleaner.Process(text)
            self.parent.queueTexts.put(text)
            self.parent.queueLinks.task_done()
            
    def Process(self, link):
        '''Непосредственно скачивание'''
        text = ''
        try:
            fd = urllib2.urlopen(link)
            stripper = TagsStripper()
            stripper.feed(fd.read())
            text = stripper.get_data()
            text = text.replace('\n', '.\n')  # так получается больше текста
            fd.close()
        except Exception:
            pass
        return text


class TextsDownloaderMonitor(threading.Thread):
    '''Монитор скачивания текста'''
    
    def __init__(self, parent):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True
        self.parent = parent
        self.queueLinksInitialSize = self.parent.queueLinks.qsize()
        
    def run(self):
        print('Monitoring started.')
        lastActionTime1 = time.time()
        lastActionTime2 = time.time()
        while self.parent.monitoring:
            '''Каждые N секунд выводим текущую информацию'''
            if time.time() - lastActionTime1 > 5:
                x = self.queueLinksInitialSize - self.parent.queueLinks.qsize()
                print('... %d/%d (%.2f%%)' % (x, self.queueLinksInitialSize, x * 100.0 / self.queueLinksInitialSize))
                lastActionTime1 = time.time()
            '''Каждые M секунд сохраняем текст'''
            if time.time() - lastActionTime2 > 60:
                self.parent.Flush()
                lastActionTime2 = time.time()
            time.sleep(1)
        print('Monitoring finished.')


class TagsStripper(HTMLParser.HTMLParser):
    '''Удалитель тегов'''
    
    def __init__(self):
        self.reset()
        self.fed = []
        self.recording = False
    
    def handle_starttag(self, tag, attributes):
        if tag == 'body':
            self.recording = True
    
    def handle_data(self, d):
        if self.recording:
            self.fed.append(d)
    
    def get_data(self):
        return ' '.join(self.fed)


class TextsCleaner(object):
    '''Чистка текста'''
    
    def __init__(self, silent = False):
        '''Инициализация'''
        self.silent = silent
        self.clearingList = []
        self.clearingList.append((re.compile(r'\n|\r'), ''))  # переводы строки
        self.clearingList.append((re.compile(r'^\s*-|-\s*'), ''))  # лишние пробелы
        self.clearingList.append((re.compile(r'[^\-a-zA-Z0-9\.,:;!\?/\(\)\[\]\\\'\"\s]'), ''))  # невалидные символы
        self.clearingList.append((re.compile(r'[\s\t]+'), ' '))  # множественные пробелы
        self.clearingList.append((re.compile(r'[\.]+'), '.'))  # множественные точки
        self.sentencesSplit = re.compile(r'\s*([\.!\?]+)\s*')  # разбивка на предложения
        self.settingsList = []
        self.settingsList.append((re.compile(r'^[^A-Z]'), 'Удалять предложения, начинающиеся не с заглавной буквы'))
        self.settingsList.append((re.compile(r'[A-Z]{2}'), 'Удалять предложения, в которых присутствует 2 и более подряд идущих заглавных букв'))
        self.settingsList.append((re.compile(r'[0-9]{3}'), 'Удалять предложения, в которых присутствует 3 и более подряд идущих цифр'))
        self.settingsList.append((re.compile(r'^.+[A-Z]'), 'Удалять предложения, в которых есть заглавные буквы не в начале предложения (обычно это имена собственные, названия и т.п.)'))
        self.settingsList.append((re.compile(r'^.{0,5}$'), 'Удалять предложения длиной менее 6 символов'))
        self.settingsList.append((re.compile(r'^([^\s]+\s?){0,4}$'), 'Удалять предложения, в которых менее 5 слов'))
        self.settingsList.append((re.compile(r'cz|sz|ej|aj'), 'Не английский язык'))
    
    def Print(self, text):
        '''Вывод текста'''
        if not self.silent:
            print(text)
    
    def Process(self, textIn, fileNameIn = None, fileNameOut = None, fileNameDebug = None):
        '''Чистим текст'''
        self.Print('Clearing started.')
        dateTimeStart = datetime.datetime.now()
        
        '''Загружаем файлы'''
        if fileNameIn != None:
            self.Print('Loading text from file ...')
            textIn = open(fileNameIn, 'r').read()
        if fileNameDebug != None:
            fdDebug = open(fileNameDebug, 'w')
        
        '''Убираем лишние символы и разбиваем на предложения'''
        self.Print('Clearing characters ...')
        for rx, replacement in self.clearingList:
            textIn = rx.sub(replacement, textIn)
        self.Print('Splitting into sentences ...')
        sentencesListAll = self.sentencesSplit.split(textIn)
        sentencesListAll = [i[:random.randint(300, 900)] + j for i, j in zip(sentencesListAll[::2], sentencesListAll[1::2])]
        self.Print('Total sentences: %d.' % len(sentencesListAll))
        
        '''Чистим по заданным правилам'''
        self.Print('Clearing sentences ...')
        counter = 0
        sentencesListGood = []
        for sentence in sentencesListAll:
            counter += 1
            if counter % 100000 == 0:
                self.Print('- %.2f %%' % (counter * 100.0 / len(sentencesListAll)))
            isGood = True
            for rx, description in self.settingsList:
                if rx.search(sentence):
                    isGood = False
                    if fileNameDebug != None:
                        fdDebug.write('%s (%s)\n' % (sentence, description))
                    break
            if isGood:
                sentencesListGood.append(sentence)
        self.Print('Good sentences: %d.' % len(sentencesListGood))
        
        '''Оставляем уникальные'''
        sentencesListGood = list(set(sentencesListGood))
        self.Print('Unique sentences: %d.' % len(sentencesListGood))
        
        '''Сохраняем'''
        textOut = '\n'.join(sentencesListGood)
        self.Print('Cleared in %d sec.' % ((datetime.datetime.now() - dateTimeStart).seconds))
        if fileNameDebug != None:
            fdDebug.close()
        if fileNameOut != None:
            self.Print('Saving text to file ...')
            open(fileNameOut, 'w').write(textOut)
            self.Print('Done.')
        else:
            self.Print('Done.')
            return textOut

if __name__ == '__main__':
    keywordsList = open(r'C:\Work\keys2\chat-clear.txt').readlines()
    random.shuffle(keywordsList)
    keywordsList = keywordsList[:2]

    folder = r'C:\Work\texts'
    linksList = LinksParser().Process(keywordsList, os.path.join(folder, 'links.txt'))
    TextsDownloader().Process(linksList, os.path.join(folder, 'texts.txt'))
