# coding=utf8
import os, random, string, re, sys, codecs, shutil, glob, datetime, urlparse
import threading, Queue, time
from common import FindMacros
from django.template.defaultfilters import slugify

class Doorgen(object):
    '''Дорген'''
    
    def __init__(self):
        '''Инициализация'''
        self.basePath = r'C:\Users\sasch\workspace\doorscenter\src\doorsagents\3rdparty\doorgen'
        self.textPath = os.path.join(self.basePath, r'text')
        self.snippetsPath = r'C:\Work\snippets'
        self.keywordsFile = os.path.join(self.basePath, r'keys\keywords.txt')
        self.netLinksFile = os.path.join(self.basePath, r'text\netlinks.txt')
        self.pageExtension = '.html'
        self.filesCache = {}
        self.validChars = "-%s%s" % (string.ascii_letters, string.digits)
        self.conversionDict = {u'а':'a',u'б':'b',u'в':'v',u'г':'g',u'д':'d',u'е':'e',u'ё':'e',u'ж':'zh',
            u'з':'z',u'и':'i',u'й':'j',u'к':'k',u'л':'l',u'м':'m',u'н':'n',u'о':'o',u'п':'p',
            u'р':'r',u'с':'s',u'т':'t',u'у':'u',u'ф':'f',u'х':'h',u'ц':'c',u'ч':'ch',u'ш':'sh',
            u'щ':'sch',u'ь':'',u'ы':'y',u'ь':'',u'э':'e',u'ю':'ju',u'я':'ja',
            u'А':'a',u'Б':'b',u'В':'v',u'Г':'g',u'Д':'d',u'Е':'e',u'Ё':'e',u'Ж':'zh',u'З':'z',
            u'И':'i',u'Й':'j',u'К':'k',u'Л':'l',u'М':'m',u'Н':'n',u'О':'o',u'П':'p',u'Р':'r',
            u'С':'s',u'Т':'t',u'У':'u',u'Ф':'f',u'Х':'h',u'Ц':'c',u'Ч':'ch',u'Ш':'sh',u'Щ':'sch',
            u'Ъ':'',u'Ы':'y',u'Ь':'',u'Э':'e',u'Ю':'ju',u'Я':'ja',
            ' ':'-'}
        self.macrosDict = {'BOSKEYWORD':self.GetPageKeyword, 'ABOSKEYWORD':self.GetPageKeyword, 'BBOSKEYWORD':self.GetPageKeyword, 'CBOSKEYWORD':self.GetPageKeyword, 
            'KEYWORD':self.GetPageKeyword, 'BKEYWORD':self.GetPageKeyword, 'BBKEYWORD':self.GetPageKeyword, 
            'RANDKEYWORD':self.GetRandomKeyword, 'ARANDKEYWORD':self.GetRandomKeyword, 'BRANDKEYWORD':self.GetRandomKeyword, 'CRANDKEYWORD':self.GetRandomKeyword, 
            'RAND_KEY':self.GetRandomKeyword, 'BRAND_KEY':self.GetRandomKeyword, 'BBRAND_KEY':self.GetRandomKeyword, 
            'RANDLINK':self.GetRandomIntLink, 'ARANDLINK':self.GetRandomIntLink, 'BRANDLINK':self.GetRandomIntLink, 'CRANDLINK':self.GetRandomIntLink, 
            'RAND_ANCOR':self.GetRandomIntLink, 'BRAND_ANCOR':self.GetRandomIntLink, 'BBRAND_ANCOR':self.GetRandomIntLink, 
            'RAND_URL':self.GetRandomIntLinkUrl, 'RANDLINKURL':self.GetRandomIntLinkUrl, 'RANDMYLINK':self.GetRandomNetLink, 
            'RANDTEXTLINE':self.GetRandomTextLine, 'SNIPPET':self.GetRandomSnippet, 'RAND':self.GetRandomNumber, 'DOR_HOST':self.GetDorHost, 
            'INDEX':self.GetIndexLink, 'INDEXLINK':self.GetIndexLink, 'SITEMAPLINK':self.GetSitemapLink, 'ALLLINK':self.GetSitemapLinks,
            'FOR':self.ProcessCycle, 'FORX':self.ProcessCycle, 
            }
    
    def _KeywordToUrl(self, keyword):
        '''Преобразование кея в URL'''
        url = ''
        if keyword != self.keywordMain:
            for c in keyword:
                if c in self.validChars:
                    url += c
                elif c in self.conversionDict:
                    url += self.conversionDict[c]
        else:
            url = 'index'
        return slugify(url) + self.pageExtension
    
    def _Capitalize(self, keyword, kind):
        '''Капитализация'''
        if kind == '':
            return keyword.lower()
        elif (kind == 'C') or (kind == 'B'):
            return keyword.capitalize()
        elif (kind == 'A') or (kind == 'BB'):
            return keyword.title()
        elif kind == 'B':
            return keyword.upper()
        else:
            return ''
        
    def _GetCachedFileLines(self, fileName):
        '''Читаем и кэшируем строки из файла'''
        if fileName not in self.filesCache:
            self.filesCache[fileName] = ['']
            if os.path.exists(fileName):
                self.filesCache[fileName] = [item.strip() for item in codecs.open(fileName, encoding='cp1251', errors='ignore').readlines()]
        return self.filesCache[fileName]
    
    '''Обработка макросов'''
    
    def GetMainKeyword(self, macrosName, macrosArgsList):
        '''Главный кейворд'''
        keyword = self.keywordMain
        kind = macrosName.replace('BOSKEYWORD', '').replace('KEYWORD', '')
        return self._Capitalize(keyword, kind)
    
    def GetPageKeyword(self, macrosName, macrosArgsList):
        '''Кейворд страницы'''
        keyword = self.keywordPage
        kind = macrosName.replace('BOSKEYWORD', '').replace('KEYWORD', '')
        return self._Capitalize(keyword, kind)
    
    def GetRandomKeyword(self, macrosName, macrosArgsList):
        '''Случайный кейворд'''
        keyword = random.choice(self.keywordsListFull)
        kind = macrosName.replace('RANDKEYWORD', '').replace('RAND_KEY', '')
        return self._Capitalize(keyword, kind)
    
    def GetRandomNumber(self, macrosName, macrosArgsList):
        '''Случайное число'''
        return str(random.randint(int(macrosArgsList[0]), int(macrosArgsList[1])))
    
    def GetRandomIntLinkUrl(self, macrosName, macrosArgsList):
        '''Случайный внутренний короткий урл'''
        keyword = random.choice(self.keywordsListFull)
        return self._KeywordToUrl(keyword)
    
    def GetRandomIntLink(self, macrosName, macrosArgsList):
        '''Случайный внутренний анкор'''
        keyword = random.choice(self.keywordsListFull)
        kind = macrosName.replace('RANDLINK', '').replace('RAND_ANCOR', '')
        return '<a href="%s">%s</a>' % (self._KeywordToUrl(keyword), self._Capitalize(keyword, kind))
    
    def GetRandomNetLink(self, macrosName, macrosArgsList):
        '''Случайная внешний анкор'''
        return random.choice(self.netLinksList)
    
    def GetRandomTextLine(self, macrosName, macrosArgsList):
        '''Случайная строка из файла'''
        fileName = os.path.join(self.textPath, macrosArgsList[0])
        return random.choice(self._GetCachedFileLines(fileName))
    
    def GetRandomSnippet(self, macrosName, macrosArgsList):
        '''Случайный сниппет'''
        fileName = os.path.join(self.snippetsPath, macrosArgsList[0])
        return random.choice(self._GetCachedFileLines(fileName))
    
    def GetIndexLink(self, macrosName, macrosArgsList):
        '''Анкор на индекс'''
        if self.keywordPage == self.keywordMain:
            return ''
        return '<a href="index%s">%s</a>' % (self.pageExtension, self.keywordMain.title())
        
    def GetSitemapLink(self, macrosName, macrosArgsList):
        '''Анкор на карту сайта'''
        if self.keywordPage != self.keywordMain:
            return ''
        return '<a href="sitemap%s">Sitemap</a>' % self.pageExtension
    
    def GetSitemapLinks(self, macrosName, macrosArgsList):
        '''Анкоры на все страницы дора для карты сайта'''
        if self.keywordPage != 'sitemap':
            return ''
        result = ''
        for keyword in self.keywordsListShort:
            result += '<a href="%s">%s</a><br/>\n' % (self._KeywordToUrl(keyword), keyword.title())
        return result
    
    def GetDorHost(self, macrosName, macrosArgsList):
        '''Хост дора'''
        return urlparse.urlparse(self.url).hostname
    
    '''Обработка страницы'''
    
    def ProcessMacrosRegex(self, m):
        '''Обрабатываем макрос, найденный регекспом'''
        macrosName =  m.groups()[0]
        if macrosName in self.macrosDict:
            macrosArgsList = m.groups()[1:]
            macrosArgsList = [self.ProcessTemplate(item) for item in macrosArgsList]
            return self.macrosDict[macrosName](macrosName, macrosArgsList)
        else:
            self.macrosUnknown.add(macrosName)
            return ''
    
    def ProcessCycle(self, macrosName, macrosArgsList, source):
        '''Обрабатываем цикл'''
        macrosEnd = '{' + macrosName.replace('FOR', 'ENDFOR') + '}'
        macrosCounter = '{I' + macrosName.replace('FOR', '') + '}'
        body, _, source = source.partition(macrosEnd)
        result = ''
        for counter in range(int(macrosArgsList[0]), int(macrosArgsList[1]) + 1):
            result += self.ProcessTemplate(body.replace(macrosCounter, str(counter)))
        return result, source
    
    def ProcessTemplate(self, source):
        '''Заменяем макросы на странице'''
        '''Процессинг циклов'''
        for macrosToProcess in ['FORX', 'FOR']:
            result = ''
            while True:
                sourceBefore, macrosName, macrosArgsList, source = FindMacros(source, macrosToProcess)
                if macrosName == '':
                    result += source
                    break
                macrosArgsList = [self.ProcessTemplate(item) for item in macrosArgsList]
                x, source = self.ProcessCycle(macrosName, macrosArgsList, source)
                result += self.ProcessTemplate(sourceBefore) + self.ProcessTemplate(x)
            source = result
        result = source
        '''Процессинг макросов без вложенности в аргументах'''
        result = re.sub(r'{([A-Z]*?)}', self.ProcessMacrosRegex, result)
        result = re.sub(r'{([A-Z]*?)\(([^{},\)]*)\)}', self.ProcessMacrosRegex, result)
        result = re.sub(r'{([A-Z]*?)\(([^{},\)]*),([^{},\)]*)\)}', self.ProcessMacrosRegex, result)
        result = re.sub(r'{([A-Z]*?)\(([^{},\)]*),([^{},\)]*),([^{},\)]*)\)}', self.ProcessMacrosRegex, result)
        result = re.sub(r'{([A-Z]*?)\(([^{},\)]*),([^{},\)]*),([^{},\)]*),([^{},\)]*)\)}', self.ProcessMacrosRegex, result)
        '''Процессинг остальных макросов'''
        '''while True:
            sourceBefore, macrosName, macrosArgsList, source = FindMacros(source)
            if macrosName == '':
                result += source
                break
            elif macrosName in self.macrosDict:
                macrosArgsList = [self.ProcessTemplate(item) for item in macrosArgsList]
                x, source = self.macrosDict[macrosName](macrosName, macrosArgsList, source)
                result += sourceBefore + self.ProcessTemplate(x)
            else:
                self.macrosUnknown.add(macrosName)
                result += sourceBefore'''
        return result
    
    def GeneratePage(self, template, keywordPage):
        '''Формируем страницу'''
        self.keywordPage = keywordPage
        pageContents = self.ProcessTemplate(template)
        pageFileName = os.path.join(self.localPath, self._KeywordToUrl(self.keywordPage))
        codecs.open(pageFileName, 'w', encoding='cp1251', errors='ignore').write(pageContents)

    def Generate(self, templatePath, pagesCount, localPath, url):
        '''Параметры генерации'''
        self.templatePath = os.path.join(self.basePath, templatePath)
        self.pagesCount = pagesCount
        self.localPath = os.path.join(self.basePath, localPath)
        self.url = url
        
        '''Начинаем'''
        dateTimeStart = datetime.datetime.now()
        self.macrosUnknown = set()
        
        '''Очищаем папку дора. Копируем все файлы из шаблона в папку дора, за исключением index.html и dp_sitemap.html'''
        if os.path.exists(self.localPath):
            shutil.rmtree(self.localPath)
        shutil.copytree(self.templatePath, self.localPath)
        for fileName in glob.glob(os.path.join(self.localPath, 'dp_*')):
            os.remove(fileName)
        
        '''Читаем кейворды и ссылки. Обрабатываем кейворды'''
        self.keywordsListFull = [item.strip() for item in codecs.open(self.keywordsFile, encoding='cp1251', errors='ignore').readlines()]
        self.keywordsListShort = self.keywordsListFull[:self.pagesCount]
        self.keywordMain = self.keywordsListShort[0]
        self.netLinksList = [item.strip() for item in codecs.open(self.netLinksFile, encoding='cp1251', errors='ignore').readlines()]
        
        '''Формируем страницы дора и карту сайта в HTML'''
        indexTemplateContents = codecs.open(os.path.join(self.templatePath, 'index.html'), encoding='cp1251', errors='ignore').read()
        for keywordPage in self.keywordsListShort:
            self.GeneratePage(indexTemplateContents, keywordPage)
        sitemapTemplateContents = codecs.open(os.path.join(self.templatePath, 'dp_sitemap.html'), encoding='cp1251', errors='ignore').read()
        self.GeneratePage(sitemapTemplateContents, 'sitemap')
        
        '''Карта сайта в XML'''
        with open(os.path.join(self.localPath, 'sitemap.xml'), 'w') as fd:
            fd.write('''<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        ''')
            for keyword in self.keywordsListShort:
                fd.write('''   <url>
              <loc>%s</loc>
              <lastmod>%s</lastmod>
              <changefreq>weekly</changefreq>
              <priority>0.5</priority>
           </url>\n''' % (self.url + self._KeywordToUrl(keyword), datetime.date.today().strftime('%Y-%m-%d')))
            fd.write('''</urlset>''')
        
        '''Отчет о проделанной работе'''
        if len(self.macrosUnknown) > 0:
            print('Unknown macros: %s.' % ', '.join(list(self.macrosUnknown)))
        print('Done in %d sec.' % (datetime.datetime.now() - dateTimeStart).seconds)


doorgen = Doorgen()
doorgen.Generate(r'templ\mamba-en', 800, r'out\jobs\door8773-new', 'http://lormont.wikidating.info/')

'''TODO:
1. add_page_key
2. STAT
'''
