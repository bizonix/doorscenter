# coding=utf8
import urllib2, re, signal, sys

'''
Тулза для анализа сеток чужих доров.

Функции:

- скачивает страницу
- собирает внутренние ссылки
- собирает внешние ссылки
- определяет число внутренних ссылок на странице
- определяет число внешних ссылок на странице
- составляет список сайтов в сетке
- получает список кейводров
- собирает текст со страниц
- собирает картинки

Чек-лист:

- обновляется ли сайт
- наличие RSS и карты сайта
- структура титла
- структура деска
- картинки: имена файлов, альты
- структура анкоров для внутренней линковки
- структура анкоров для внешней линковки
- титлы в ссылках
- категории, их число
- ссылки на "левые" сайты

'''

rxTitle = re.compile(r'<title>(.*?)</title>', re.I)
rxDescription = re.compile(r'<meta\s*?name="description"\s*?content="(.*?)"\s*?/?>', re.I)
rxLinks = re.compile(r'<a\s.*?href\s*?=\s*?([^\s>]*).*?>(.*?)</a>', re.I)
rxImages = re.compile(r'<img\s.*?src="(.*?)"')

class Crawler(object):
    
    def __init__(self):
        ''''''
        self.Init()
    
    def IsSiteNeeded(self, url):
        '''Определяем, принадлежит ли сайт нужной сетке'''
        if not url.startswith('http://'):
            return False
        html = urllib2.urlopen(url).read()
        return html.find('function adultdating(') >= 0
    
    def GetPage(self, site, url):
        '''Скачиваем страницу и получаем из нее: 
        титл, деск, внутренние и внешние ссылки, анкоры, ...'''
        print('Getting %s...' % url)
        '''Получаем страницу'''
        html = urllib2.urlopen(url).read()
        '''Получаем титл, деск и кейворды'''
        title = ''.join(rxTitle.findall(html))
        description = ''.join(rxDescription.findall(html))
        for keyword in description.lower().split(','):
            keyword = keyword.strip()
            if keyword not in self.keywords:
                self.keywords.append(keyword)
        '''Получаем ссылки'''
        links = rxLinks.findall(html)
        internalLinksCount = 0
        externalLinksCount = 0
        for link, anchor in links:
            '''Приводим ссылку к нормальному виду'''
            link = link.lower()
            if link[0] in ['\'', '"'] and link[-1] in ['\'', '"']:
                link = link[1:-1]
            if link.find('#') >= 0:
                link = link[:link.find('#')]
            if link.find('http://') < 0:
                link = site + link
            linkSite = link[:(link + '///').find('/', 7) + 1]
            anchor = anchor.lower()
            '''Удаляем ненужное'''
            if link == '' or link.startswith('index.') or link.endswith('.xml') or link.endswith('.rss') or link.find('<') >= 0 or link.find('wordpress') >= 0 or link.find('wp-') >= 0:
                continue
            '''Считаем ссылки'''
            if link.startswith(site):
                internalLinksCount += 1
            else:
                externalLinksCount += 1
            '''Еще раз удаляем ненужное'''
            if (link in self.internalLinksQueue) or (link in self.internalLinksProcessed) or (linkSite in self.externalLinksQueue) or (link in self.otherLinks):
                continue
            '''Добавляем нужное в очередь'''
            if link.startswith(site):
                self.internalLinksQueue.append(link)
            elif self.IsSiteNeeded(linkSite):
                self.externalLinksQueue.append(linkSite)
            else:
                self.otherLinks.append(link)
            if anchor.find('<') < 0:
                self.anchors.append(anchor)
        '''Информация о странице'''
        self.pagesInternal.append((url, title, description, internalLinksCount, externalLinksCount))
        print(self.pagesInternal[-1])
        print('\n'.join(self.otherLinks))
        #print(html)
    
    def ShowResults(self):
        print('Pages:\n%s\n' % '\n'.join(self.pagesInternal))
        print('Keywords:\n%s\n' % '\n'.join(self.keywords))
        print('Internal links queue:\n%s\n' % '\n'.join(self.internalLinksQueue))
        print('Internal links processed:\n%s\n' % '\n'.join(self.internalLinksProcessed))
        print('External links queue:\n%s\n' % '\n'.join(self.externalLinksQueue))
        print('Other links:\n%s\n' % '\n'.join(self.otherLinks))
        print('Anchors:\n%s\n' % '\n'.join(self.anchors))
    
    def Init(self):
        '''Инициализация кролинга'''
        self.pagesInternal = []
        self.keywords = []
        self.internalLinksQueue = []
        self.internalLinksProcessed = []
        self.externalLinksQueue = []
        self.otherLinks = []
        self.anchors = []
        
    def Main(self, startUrl):
        '''Главная процедура кролинга'''
        self.Init()
        site = startUrl
        self.internalLinksQueue.append(site)
        while len(self.internalLinksQueue) > 0:
            url = self.internalLinksQueue.pop()
            self.GetPage(site, url)
            self.internalLinksProcessed.append(url)
            print('keys: %d, int queue: %d, int proc: %d, ext queue: %d, others: %d.' % (len(self.keywords), len(self.internalLinksQueue), len(self.internalLinksProcessed), len(self.externalLinksQueue), len(self.otherLinks)))
        self.ShowResults()

#crawler = Crawler()
#crawler.Main('http://www.crazydreamlover.com/')

rxText = re.compile(r'<p align="center">(.*?)</p>', re.M | re.S)
rxComments = re.compile(r'<div class="comment-content"><p>(.*?)</p>', re.M | re.S)

url = 'http://www.davidheaven.com/adult-sex-holiday-sexy-married-girls-fordoche.html'
html = urllib2.urlopen(url).read()
text = '==='.join(rxText.findall(html))
print('###' + text)
comments = '==='.join(rxComments.findall(html))
print('###' + comments)
