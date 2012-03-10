# coding=utf8
import os, glob, re, random, urllib2
from xml.etree import ElementTree

class Page(object):
    '''Страница (абстрактный класс)'''
    
    def __init__(self, url):
        '''Инициализация'''
        self.url = url
        self.title = None
        self.ResetWeight()
    
    def ResetWeight(self):
        '''Сбрасываем вес к дефолтному значению'''
        self.weight = 1.0
    

class PageInternal(Page):
    '''Внутренняя страница'''
    
    def __init__(self, url):
        '''Инициализация'''
        Page.__init__(self, url)
        self.linksInternalOut = []  # исходящие ссылки на другие внутренние страницы
        self.linksInternalIn = []  # входящие ссылки с других внутренних страниц
        self.linksExternalOut = []  # исходящие ссылки на внешние страницы

    def UpdateWeight(self, method):
        '''Пересчитываем вес'''
        d = 0.85
        if method == 1:  # метод из page-weight.ru
            for linkInternal in self.linksInternalOut:
                linkInternal.pageTo.weight += self.weight * d / (len(self.linksInternalOut) + len(self.linksExternalOut))
        elif method == 2:  # правильный метод
            summa = 0.0
            for linkInternal in self.linksInternalIn:
                pageFrom = linkInternal.pageFrom
                summa += pageFrom.weight / (len(pageFrom.linksInternalOut) + len(pageFrom.linksExternalOut))
            self.weight = 1 - d + d * summa

    def NormalizeWeight(self, method, maxWeight):
        '''Нормализуем вес'''
        if method == 1:
            self.weight *= 100.0 / maxWeight


class PageExternal(Page):
    '''Внешняя страница'''
    
    def __init__(self, url):
        '''Инициализация'''
        Page.__init__(self, url)
        self.linksInternalIn = []  # входящие ссылки с внутренних страниц


class Link(object):
    '''Ссылка'''
    
    def __init__(self, pageFrom, pageTo, anchor):
        '''Инициализация'''
        self.pageFrom = pageFrom
        self.pageTo = pageTo
        self.anchor = anchor
        

class Pages(object):
    '''Страницы сайта'''
        
    def __init__(self, baseUrl):
        '''Инициализация'''
        self.baseUrl = baseUrl
        self.pagesInternal = set()
        self.pagesExternal = set()
        
    def _IsUrlInternal(self, url):
        '''Принадлежит ли URL этому сайту'''
        return url.replace(self.baseUrl, '').find('/') < 0
        
    def FindPage(self, url):
        '''Находим в наборах страницу по ее URL'''
        for page in self.pagesInternal:
            if page.url == url:
                return page
        for page in self.pagesExternal:
            if page.url == url:
                return page
        return None
        
    def GetOrCreatePage(self, url, title = None):
        '''Получаем (и создаем, если ее нет) страницу по ее URL'''
        page = self.FindPage(url)
        if page == None:
            if url.endswith('.php'):
                raise('')
            if self._IsUrlInternal(url):
                '''Создаем новую внутреннюю страницу'''
                page = PageInternal(url)
                self.pagesInternal.add(page)
            else:
                '''Создаем новую внешнюю страницу'''
                page = PageExternal(url)
                self.pagesExternal.add(page)
        if (page.title == None) and (title != None):
            '''Апдейтим title'''
            page.title = title
        return page
            
    def AddLink(self, pageFrom, pageTo, anchor = None):
        '''Добавляем ссылку'''
        link = Link(pageFrom, pageTo, anchor)
        if isinstance(pageTo, PageInternal):
            pageFrom.linksInternalOut.append(link)
        else:
            pageFrom.linksExternalOut.append(link)
        pageTo.linksInternalIn.append(link)
    
    def AddLinkDual(self, page1, page2, anchor = None):
        '''Добавляем двунаправленную ссылку'''
        self.AddLink(page1, page2, anchor)
        self.AddLink(page2, page1, anchor)
        
    def Analyze(self):
        '''Рассчитываем page weight'''
        print('Calculating page weights ...')
        for _ in range(int(len(self.pagesInternal) * 0.2)):  # удаляем часть страниц, типа нет в индексе
            self.pagesInternal.remove(random.sample(self.pagesInternal, 1)[0])
        method = 2
        iterations = 10
        for _ in range(iterations):  # цикл по итерациям
            for page in self.pagesInternal:  # цикл по страницам
                page.UpdateWeight(method)  # апдейтим вес
        if method == 1:
            maxWeight = max(self.pagesInternal, key=lambda item: item.weight).weight
            for page in self.pagesInternal:  # нормализация веса
                page.NormalizeWeight(method, maxWeight)
        '''Результаты'''
        print('')
        print('Internal pages:')
        #pagesInternalSorted = sorted(self.pagesInternal, key=lambda item: item.weight, reverse=True)
        pagesInternalSorted = sorted(self.pagesInternal, key=lambda item: item.url, reverse=False)
        for page in pagesInternalSorted[:50]:
            print('/{0:<50} - in: {1:>3}; out: {2:>3}; outex: {3:>2}; weight: {4:>6.2f}'.format(page.url.replace(self.baseUrl, ''), len(page.linksInternalIn), len(page.linksInternalOut), len(page.linksExternalOut), page.weight))
        print('')
        print('External pages:')
        pagesExternalSorted = sorted(self.pagesExternal, key=lambda item: len(item.linksInternalIn), reverse=True)
        for page in pagesExternalSorted[:50]:
            print('{0:<80} - in: {1:>3}'.format(page.url, len(page.linksInternalIn)))

    def Generate(self):
        '''Создаем структуру страниц вручную'''
        '''Все страницы'''
        pagesCount = 30
        pagesList = []
        for n in range(pagesCount):
            pagesList.append(self.GetOrCreatePage('%03d.html' % (n + 1)))
        '''Индекс и карта'''
        indexPage = pagesList[0]
        sitemapPage = pagesList[1]
        pagesList = pagesList[2:]
        '''Категории'''
        categoriesCount = 3
        categoriesList = pagesList[:categoriesCount]
        pagesList = pagesList[categoriesCount:]
        '''Расставляем ссылки'''
        self.AddLink(indexPage, sitemapPage)  # с главной на карту
        self.AddLink(sitemapPage, indexPage)  # с карты на главную
        for categoryPage in categoriesList:  
            self.AddLink(indexPage, categoryPage)  # с главной на категории
            self.AddLink(sitemapPage, categoryPage)  # с карты на категории
        if categoriesCount > 0:
            for page in pagesList:
                self.AddLink(random.choice(categoriesList), page)  # с категорий на страницы
        for page in pagesList:
            self.AddLink(sitemapPage, page)  # с карты на страницы
        cyclesCount = 3
        for _ in range(cyclesCount):  # кольца страниц
            random.shuffle(pagesList)
            for n in range(len(pagesList)):
                self.AddLink(pagesList[n], pagesList[(n + 1) % len(pagesList)])
                self.AddLink(pagesList[n], pagesList[(n + 2) % len(pagesList)])
                self.AddLink(pagesList[n], pagesList[(n - 1) % len(pagesList)])
                self.AddLink(pagesList[n], pagesList[(n - 2) % len(pagesList)])
        makeRandom = 1
        if makeRandom > 0:
            for page in pagesList:  # хаотичная перелинковка страниц
                for _ in range(random.randint(3, 5)):
                    self.AddLink(page, random.choice(pagesList))
    
        
class Site(object):
    '''Сайт'''
    
    def __init__(self, baseUrl, localFolder):
        '''Инициализация'''
        self.baseUrl = baseUrl
        if self.baseUrl[-1] != '/':
            self.baseUrl += '/'
        self.localFolder = localFolder
        self.pages = Pages(baseUrl)
        
    def _NormalizeUrl(self, url):
        '''Приводим URL к нормальному виду'''
        url = url.lower().strip()
        if url[0] in ['\'', '"'] and url[-1] in ['\'', '"']:
            url = url[1:-1]
        if url.find('#') >= 0:
            url = url[:url.find('#')]
        if url.find('?') >= 0:
            url = url[:url.find('?')]
        if url.find('http://') < 0:
            url = self.baseUrl + url
        indexPages = ['index.html']
        for indexPage in indexPages:
            if url.endswith('/' + indexPage):
                url = url[:-len(indexPage)]
                break
        return url.strip()
        
    def DownloadBySitemap(self):  # не доделано
        '''Скачиваем по XML карте сайта'''
        sitemapUrl = os.path.join(self.baseUrl, 'sitemap.xml')
        sitemapText = urllib2.urlopen(sitemapUrl).read()
        sitemapXml = ElementTree.XML(sitemapText)
        urlsList = []
        for element1 in sitemapXml:
            for element2 in element1:
                if element2.tag.endswith('loc'):
                    urlsList.append(element2.text.strip())
        print('Urls in sitemap: %d' % len(urlsList))
        
    
    def Load(self):
        '''Парсим сайт с диска'''
        rxTitle = re.compile(r'<title>(.*?)</title>', re.I)
        rxLinks = re.compile(r'<a\s.*?href\s*?=\s*?([^\s>]*).*?>(.*?)</a>', re.I)
        print('Loading site ...')
        for fileName in glob.glob(os.path.join(self.localFolder, '*.*')):
            '''Читаем страницу'''
            pageUrl = self._NormalizeUrl(os.path.join(self.baseUrl, os.path.basename(fileName)))
            if not (pageUrl.endswith('.html') or pageUrl.endswith('/')):
                continue
            pageHtml = open(fileName).read()
            pageTitle = ''.join(rxTitle.findall(pageHtml))
            page = self.pages.GetOrCreatePage(pageUrl, pageTitle)
            linkUrlsProcessed = set()
            for linkUrl, linkAnchor in rxLinks.findall(pageHtml):
                '''Приводим URL и анкор к нормальному виду'''
                linkUrl = self._NormalizeUrl(linkUrl)
                if not (linkUrl.endswith('.html') or linkUrl.endswith('/')):
                    continue
                if linkUrl in linkUrlsProcessed:
                    continue
                linkAnchor = linkAnchor.lower()
                '''Добавляем ссылку'''
                linkPage = self.pages.GetOrCreatePage(linkUrl)
                self.pages.AddLink(page, linkPage, linkAnchor)
                linkUrlsProcessed.add(linkUrl)
        return self.pages
    
if __name__ == '__main__':
    #site = Site('http://fastfreedating.info/', r'C:\Temp\wget\datingwater.info')
    #site = Site('http://www.davidheaven.com/', r'C:\Temp\wget\www.davidheaven.com')
    #site.DownloadBySitemap()
    #site = Site('http://www.alonsoracing.com/', r'C:\Temp\wget\www.alonsoracing.com')
    #site.DownloadBySitemap()
    #pages = site.Load()
    pages = Pages('http://test.com/')
    pages.Generate()
    pages.Analyze()
