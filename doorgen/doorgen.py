# coding=utf8
import os, random, string, re, codecs, shutil, glob, datetime, urlparse
from common import FindMacros
from doorway import Doorway
from django.template.defaultfilters import slugify
import cProfile, pstats

class Doorgen(object):
    '''Дорген'''
    
    def __init__(self, templatesPath, textPath, snippetsPath):
        '''Инициализация'''
        self.basePath = r'C:\Users\sasch\workspace\doorscenter\src\doorsagents\3rdparty\doorgen'
        self.templatesPath = os.path.join(self.basePath, r'templ')
        self.textPath = os.path.join(self.basePath, r'text')
        self.snippetsPath = r'C:\Work\snippets'
        self.pageExtension = '.html'
        self.rx0 = re.compile(r'{([A-Z0-9_/]*?)}')
        self.rx1 = re.compile(r'{([A-Z0-9_/]*?)\(([^{},\)]*)\)}')
        self.rx2 = re.compile(r'{([A-Z0-9_/]*?)\(([^{},\)]*),([^{},\)]*)\)}')
        
        self.validChars = "-%s%s" % (string.ascii_letters, string.digits)
        self.conversionDict = {u'а':'a',u'б':'b',u'в':'v',u'г':'g',u'д':'d',u'е':'e',u'ё':'e',u'ж':'zh',
            u'з':'z',u'и':'i',u'й':'j',u'к':'k',u'л':'l',u'м':'m',u'н':'n',u'о':'o',u'п':'p',
            u'р':'r',u'с':'s',u'т':'t',u'у':'u',u'ф':'f',u'х':'h',u'ц':'c',u'ч':'ch',u'ш':'sh',
            u'щ':'sch',u'ь':'',u'ы':'y',u'ь':'',u'э':'e',u'ю':'ju',u'я':'ja',
            u'А':'a',u'Б':'b',u'В':'v',u'Г':'g',u'Д':'d',u'Е':'e',u'Ё':'e',u'Ж':'zh',u'З':'z',
            u'И':'i',u'Й':'j',u'К':'k',u'Л':'l',u'М':'m',u'Н':'n',u'О':'o',u'П':'p',u'Р':'r',
            u'С':'s',u'Т':'t',u'У':'u',u'Ф':'f',u'Х':'h',u'Ц':'c',u'Ч':'ch',u'Ш':'sh',u'Щ':'sch',
            u'Ъ':'',u'Ы':'y',u'Ь':'',u'Э':'e',u'Ю':'ju',u'Я':'ja',' ':'-'}
        self.macrosDict = {
            'DOORKEYWORD':self.GetMainKeyword, 'ADOORKEYWORD':self.GetMainKeyword, 'BDOORKEYWORD':self.GetMainKeyword, 'CDOORKEYWORD':self.GetMainKeyword, 
            'BOSKEYWORD':self.GetPageKeyword, 'ABOSKEYWORD':self.GetPageKeyword, 'BBOSKEYWORD':self.GetPageKeyword, 'CBOSKEYWORD':self.GetPageKeyword, 
            'RANDKEYWORD':self.GetRandomKeyword, 'ARANDKEYWORD':self.GetRandomKeyword, 'BRANDKEYWORD':self.GetRandomKeyword, 'CRANDKEYWORD':self.GetRandomKeyword, 
            'RANDLINK':self.GetRandomIntLink, 'ARANDLINK':self.GetRandomIntLink, 'BRANDLINK':self.GetRandomIntLink, 'CRANDLINK':self.GetRandomIntLink, 
            'RANDLINKURL':self.GetRandomIntLinkUrl, 'RANDMYLINK':self.GetRandomNetLink, 'RANDTEXTLINE':self.GetRandomTextLine, 'SNIPPET':self.GetRandomSnippet, 
            'RAND':self.GetRandomNumber, 'COUNTRAND':self.GetLastRandomNumber, 'DOR_HOST':self.GetDorHost, 'VARIATION':self.GetVariation, 
            'INDEXLINK':self.GetIndexLink, 'SITEMAPLINK':self.GetSitemapLink, 'ALLLINK':self.GetSitemapLinks}
    
    def _KeywordToUrl(self, keyword):
        '''Преобразование кея в URL'''
        if keyword == self.keywordDoor:
            return 'index' + self.pageExtension
        if keyword not in self.keywordsUrlDict:
            url = ''
            for c in keyword:
                if c in self.validChars:
                    url += c
                elif c in self.conversionDict:
                    url += self.conversionDict[c]
            self.keywordsUrlDict[keyword] = slugify(url) + self.pageExtension
        return self.keywordsUrlDict[keyword]
    
    def _Capitalize(self, keyword, kind):
        '''Капитализация'''
        if kind == '':
            if keyword not in self.keywordsLowerDict:
                self.keywordsLowerDict[keyword] = keyword.lower()
            return self.keywordsLowerDict[keyword]
        elif kind == 'A':
            if keyword not in self.keywordsTitleDict:
                self.keywordsTitleDict[keyword] = keyword.title()
            return self.keywordsTitleDict[keyword]
        elif kind == 'B':
            if keyword not in self.keywordsUpperDict:
                self.keywordsUpperDict[keyword] = keyword.upper()
            return self.keywordsUpperDict[keyword]
        elif kind == 'C':
            if keyword not in self.keywordsCapitDict:
                self.keywordsCapitDict[keyword] = keyword.capitalize()
            return self.keywordsCapitDict[keyword]
        else:
            return ''
        
    def _GetFileContents(self, fileName, makePreprocess = False):
        '''Читаем содержимое файла'''
        contents = codecs.open(fileName, encoding='cp1251', errors='ignore').read()
        if makePreprocess:
            contents = self.PreprocessTemplate(contents)
        return contents
    
    def _GetCachedFileLines(self, fileName, makePreprocess = False):
        '''Читаем и кэшируем строки из файла'''
        if fileName not in self.filesCache:
            self.filesCache[fileName] = ['']
            if os.path.exists(fileName):
                self.filesCache[fileName] = [item.strip() for item in self._GetFileContents(fileName, makePreprocess).split('\n')]
        return self.filesCache[fileName]
    
    '''Обработка макросов'''
    
    def GetMainKeyword(self, macrosName, macrosArgsList):
        '''Главный кейворд'''
        keyword = self.keywordDoor
        kind = macrosName[:-11]
        return self._Capitalize(keyword, kind)
    
    def GetPageKeyword(self, macrosName, macrosArgsList):
        '''Кейворд страницы'''
        keyword = self.keywordPage
        kind = macrosName[:-10]
        return self._Capitalize(keyword, kind)
    
    def GetRandomKeyword(self, macrosName, macrosArgsList):
        '''Случайный кейворд'''
        keyword = random.choice(self.keywordsListFull)
        kind = macrosName[:-11]
        return self._Capitalize(keyword, kind)
    
    def GetRandomNumber(self, macrosName, macrosArgsList):
        '''Случайное число'''
        self.lastRandomNumber = random.randint(int(macrosArgsList[0]), int(macrosArgsList[1]))
        return str(self.lastRandomNumber)
    
    def GetLastRandomNumber(self, macrosName, macrosArgsList):
        '''Предыдущее случайное число'''
        return str(self.lastRandomNumber)
    
    def GetRandomIntLinkUrl(self, macrosName, macrosArgsList):
        '''Случайный внутренний короткий урл'''
        keyword = random.choice(self.keywordsListShort)
        return self._KeywordToUrl(keyword)
    
    def GetRandomIntLink(self, macrosName, macrosArgsList):
        '''Случайный внутренний анкор'''
        keyword = random.choice(self.keywordsListShort)
        kind = macrosName[:-8]
        return '<a href="%s">%s</a>' % (self._KeywordToUrl(keyword), self._Capitalize(keyword, kind))
    
    def GetRandomNetLink(self, macrosName, macrosArgsList):
        '''Случайная внешний анкор'''
        return random.choice(self.netLinksList)
    
    def GetRandomTextLine(self, macrosName, macrosArgsList):
        '''Случайная строка из файла'''
        fileName = os.path.join(self.textPath, macrosArgsList[0])
        return random.choice(self._GetCachedFileLines(fileName, True))
    
    def GetRandomSnippet(self, macrosName, macrosArgsList):
        '''Случайный сниппет'''
        fileName = os.path.join(self.snippetsPath, macrosArgsList[0])
        return random.choice(self._GetCachedFileLines(fileName, True))
    
    def GetIndexLink(self, macrosName, macrosArgsList):
        '''Анкор на индекс'''
        if self.keywordPage == self.keywordDoor:
            return ''
        return '<a href="index%s">%s</a>' % (self.pageExtension, self._Capitalize(self.keywordDoor, 'A'))
        
    def GetSitemapLink(self, macrosName, macrosArgsList):
        '''Анкор на карту сайта'''
        if self.keywordPage != self.keywordDoor:
            return ''
        return '<a href="sitemap%s">Sitemap</a>' % self.pageExtension
    
    def GetSitemapLinks(self, macrosName, macrosArgsList):
        '''Анкоры на все страницы дора для карты сайта'''
        if self.keywordPage != 'sitemap':
            return ''
        result = ''
        for keyword in self.keywordsListShort:
            result += '<a href="%s">%s</a><br/>\n' % (self._KeywordToUrl(keyword), self._Capitalize(keyword, 'A'))
        return result
    
    def GetDorHost(self, macrosName, macrosArgsList):
        '''Хост дора'''
        return urlparse.urlparse(self.doorway.url).hostname
    
    def GetVariation(self, macrosName, macrosArgsList):
        '''Вариация'''
        return random.choice(macrosArgsList[0].split('|'))
    
    '''Обработка страницы'''
    
    def ProcessMacrosRegex(self, m):
        '''Обрабатываем макрос, найденный регекспом'''
        macrosName =  m.groups()[0]
        if macrosName in self.macrosDict:
            macrosArgsList = m.groups()[1:]
            macrosArgsList = [self.ProcessTemplate(item) for item in macrosArgsList]
            return self.ProcessTemplate(self.macrosDict[macrosName](macrosName, macrosArgsList))
        else:
            self.macrosUnknown.add(m.group(0))
            return ''
    
    def ProcessTemplate(self, template):
        '''Процессинг циклов'''
        for macrosToProcess in ['FORX', 'FOR']:
            if template.find('{') < 0:
                return template
            templateBefore, _, macrosName, macrosArgsList, template = FindMacros(template, macrosToProcess)
            if macrosName != '':
                macrosArgsList = [self.ProcessTemplate(item) for item in macrosArgsList]
                macrosNameEnd = '{' + macrosName.replace('FOR', 'ENDFOR') + '}'
                macrosCounter = '{I' + macrosName.replace('FOR', '') + '}'
                body, _, rest = template.partition(macrosNameEnd)
                template = self.ProcessTemplate(templateBefore)
                for counter in range(int(macrosArgsList[0]), int(macrosArgsList[1]) + 1):
                    template += self.ProcessTemplate(body.replace(macrosCounter, str(counter)))
                template += self.ProcessTemplate(rest)
        '''Быстрый процессинг макросов регекспами'''
        if template.find('{') < 0:
            return template
        template = self.rx0.sub(self.ProcessMacrosRegex, template)
        if template.find('{') < 0:
            return template
        template = self.rx1.sub(self.ProcessMacrosRegex, template)
        if template.find('{') < 0:
            return template
        template = self.rx2.sub(self.ProcessMacrosRegex, template)
        '''Процессинг остальных макросов'''
        while True:
            if template.find('{') < 0:
                return template
            templateBefore, macrosFull, macrosName, macrosArgsList, template = FindMacros(template)
            if macrosName == '':
                break
            if macrosName in self.macrosDict:
                macrosArgsList = [self.ProcessTemplate(item) for item in macrosArgsList]
                template = templateBefore + self.ProcessTemplate(self.macrosDict[macrosName](macrosName, macrosArgsList)) + template
            else:
                self.macrosUnknown.add(macrosFull)
                template = templateBefore + template
        return template
    
    def PreprocessTemplate(self, template):
        '''Препроцессинг шаблона страницы'''
        template = template.replace('{STAT}{RANDKEYWORD}{/STAT}', '{DOORKEYWORD}').replace('{STAT}{ARANDKEYWORD}{/STAT}', '{ADOORKEYWORD}')
        template = template.replace('{STAT}{BRANDKEYWORD}{/STAT}', '{BDOORKEYWORD}').replace('{STAT}{CRANDKEYWORD}{/STAT}', '{CDOORKEYWORD}')
        template = template.replace('{MKEYWORD}', '{DOORKEYWORD}').replace('{BMKEYWORD}', '{CDOORKEYWORD}').replace('{BBMKEYWORD}', '{ADOORKEYWORD}')
        template = template.replace('{KEYWORD}', '{BOSKEYWORD}').replace('{BKEYWORD}', '{CBOSKEYWORD}').replace('{BBKEYWORD}', '{ABOSKEYWORD}')
        template = template.replace('{RAND_KEY}', '{RANDKEYWORD}').replace('{BRAND_KEY}', '{CRANDKEYWORD}').replace('{BBRAND_KEY}', '{ARANDKEYWORD}')
        template = template.replace('{RAND_ANCOR}', '{RANDLINK}').replace('{BRAND_ANCOR}', '{CRANDLINK}').replace('{BBRAND_ANCOR}', '{ARANDLINK}')
        template = template.replace('{RAND_URL}', '{RANDLINKURL}')
        template = template.replace('{INDEX}', '{INDEXLINK}')
        template = template.replace('{PIWIK}', '')
        template = template.replace('[[', '{VARIATION(').replace(']]', ')}')
        return template
    
    def GeneratePage(self, template, keywordPage):
        '''Формируем страницу'''
        self.keywordPage = keywordPage
        pageContents = self.ProcessTemplate(template)
        pageFileName = self._KeywordToUrl(keywordPage)
        self.doorway.AddPage(pageFileName, pageContents)
        '''Добавляем в список страниц'''
        link = '<a href="http://%s/%s">%s</a>' % (self.doorway.url, pageFileName, self._Capitalize(keywordPage, ''))
        if keywordPage != 'sitemap':
            self.pageLinksList.append(link)
        else:
            self.pageLinksList.insert(1, link)

    def Generate(self, keywordsList, netLinksList, template, pagesCount, url):
        '''Генерируем дор'''
        templatePath = os.path.join(self.templatesPath, template)
        
        '''Инициализация'''
        print('Generating ...')
        dateTimeStart = datetime.datetime.now()
        self.filesCache = {}
        self.keywordsUrlDict = {}
        self.keywordsLowerDict = {}
        self.keywordsUpperDict = {}
        self.keywordsTitleDict = {}
        self.keywordsCapitDict = {}
        self.lastRandomNumber = 0;
        self.macrosUnknown = set()

        self.keywordsListFull = [item.strip() for item in keywordsList]
        self.keywordsListShort = self.keywordsListFull[:pagesCount]
        self.keywordDoor = self.keywordsListShort[0]
        self.netLinksList = [item.strip() for item in netLinksList]
        self.pageLinksList = []
        
        '''Начинаем создание дора'''
        self.doorway = Doorway(url)
        self.doorway.InitTemplate(templatePath)
        
        '''Формируем страницы дора и карту сайта в HTML'''
        indexTemplateContents = self._GetFileContents(os.path.join(templatePath, 'index.html'), True)
        for keywordPage in self.keywordsListShort:
            self.GeneratePage(indexTemplateContents, keywordPage)
        sitemapTemplateContents = self._GetFileContents(os.path.join(templatePath, 'dp_sitemap.html'), True)
        self.GeneratePage(sitemapTemplateContents, 'sitemap')
        
        '''Карта сайта в XML'''
        sitemap = '''<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'''
        for keyword in self.keywordsListShort:
            sitemap += '''  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.5</priority>\n  </url>\n''' % (url + self._KeywordToUrl(keyword), datetime.date.today().strftime('%Y-%m-%d'))
        sitemap += '''</urlset>'''
        self.doorway.AddPage('sitemap.xml', sitemap)
        
        '''Отчет о проделанной работе'''
        if len(self.macrosUnknown) > 0:
            print('Unknown macros (%d): %s.' % (len(self.macrosUnknown), ', '.join(list(self.macrosUnknown))))
        print('Done in %d sec.' % (datetime.datetime.now() - dateTimeStart).seconds)
        return self.doorway

def Test():
    templatesPath = r'C:\Users\sasch\workspace\doorscenter\src\doorsagents\3rdparty\doorgen\templ'
    textPath = r'C:\Users\sasch\workspace\doorscenter\src\doorsagents\3rdparty\doorgen\text'
    snippetsPath = r'C:\Work\snippets'
    keywordsList = codecs.open(r'C:\Users\sasch\workspace\doorscenter\src\doorsagents\3rdparty\doorgen\keys\keywords.txt', encoding='cp1251', errors='ignore').readlines()
    netLinksList = codecs.open(r'C:\Users\sasch\workspace\doorscenter\src\doorsagents\3rdparty\doorgen\text\netlinks.txt', encoding='cp1251', errors='ignore').readlines()
    
    doorgen = Doorgen(templatesPath, textPath, snippetsPath)
    doorway = doorgen.Generate(keywordsList, netLinksList, 'mamba-en', 800, 'http://oneshop.info/123')
    #doorway.UploadToFTP('searchpro.name', 'defaultx', 'n5kh9yLm', '/public_html/oneshop.info/web/123')

if __name__ == '__main__':
    Test()
    #cProfile.run('Test()', 'profiling')
    '''p = pstats.Stats('profiling')
    p.print_callers()
    p.sort_stats('time')
    p.print_stats()'''


'''TODO:
1. add_page_key
2. разные даты в карте сайта xml
3. оставлять неизвестные макросы
4. Список последовательно выполняемыех макросов.

'''
