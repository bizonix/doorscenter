# coding=utf8

import urllib, urllib2
from xml.etree import ElementTree

'''
1. В выдаче находит доры по редиректу.
2. Анализ доров:
- возраст домена
- индекс в гугле
- ссылки по гуглу
- наличие sitemap.xml, sitemap.html, map.html
- если есть sitemap.xml, то:
--- число страниц
--- сайт скачивается полностью
--- анализируется внутренняя линковка
- N страниц берутся рандомно из ссылок в исходной странице, для них отображаются:
--- урлы
--- титлы
--- дески
--- кейворды
--- число ссылок на внутренние
--- число ссылок на внешние
--- анкоры ссылок на внутренние
- для найденной страницы отображаются:
--- тошнота и плотность кеев
--- процент кеев
'''

class DoorExplorer(object):
    '''Анализ (чужого) дора'''
    
    def __init__(self, pageUrl):
        '''Инициализация'''
        self.pageUrl = pageUrl  # страница, с которой начинаем анализ
        self.rootUrl = self.GetRootUrl(self.pageUrl)  # корень дора
        
    @classmethod
    def BoolToYesNo(self, value):
        '''Конвертируем тип Boolean в строки "yes" и "no"'''
        return 'yes' if value else 'no'
    
    @classmethod
    def GetRootUrl(self, url):
        '''Находим корень сайта. Текущая реализация - возвращает корень домена'''
        return url[:(url[7:].find('/') + 8)]
        
    @classmethod
    def GetStatusCode(self, url):
        '''Получаем код статуса урла'''
        return urllib.urlopen(url).getcode()
    
    def HasSitemapXML(self):
        '''Есть ли карта сайта в XML'''
        self.hasSitemapXML = self.GetStatusCode(self.rootUrl + 'sitemap.xml') == 200
        return self.hasSitemapXML

    def HasSitemapHTML(self):
        '''Есть ли карта сайта в HTML'''
        self.hasSitemapHTML = False
        if self.GetStatusCode(self.rootUrl + 'sitemap.html') == 200:
            self.hasSitemapHTML = True
        elif self.GetStatusCode(self.rootUrl + 'sitemap.htm') == 200:
            self.hasSitemapHTML = True
        elif self.GetStatusCode(self.rootUrl + 'map.html') == 200:
            self.hasSitemapHTML = True
        elif self.GetStatusCode(self.rootUrl + 'map.htm') == 200:
            self.hasSitemapHTML = True
        return self.hasSitemapHTML

    def ProcessSitemapXML(self):
        '''Скачиваем карту сайта'''
        sitemapUrl = self.rootUrl + 'sitemap.xml'
        sitemapText = urllib2.urlopen(sitemapUrl).read()
        sitemapXml = ElementTree.XML(sitemapText)
        self.pageUrlsList = []
        for element1 in sitemapXml:
            for element2 in element1:
                if element2.tag.endswith('loc'):
                    self.pageUrlsList.append(element2.text.strip())

    def Analyze(self):
        '''Анализ дора'''
        print('Start URL: %s' % self.pageUrl)
        print('Root URL: %s' % self.rootUrl)
        print('Sitemap HTML: %s' % self.BoolToYesNo(self.HasSitemapHTML()))
        print('Sitemap XML: %s' % self.BoolToYesNo(self.HasSitemapXML()))
        if self.hasSitemapXML:
            self.ProcessSitemapXML()
            print('Pages count in sitemap.xml: %d' % len(self.pageUrlsList))
            '''Здесь будет анализ линковки'''

explorer = DoorExplorer('http://www.davidheaven.com/adult-sex-holiday-sexy-married-girls-fordoche.html')
explorer.Analyze()
