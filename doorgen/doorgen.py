# coding=utf8
import os, random, string, re, codecs, shutil, glob, datetime, urlparse
from common import FindMacros
from django.template.defaultfilters import slugify
import cProfile

class Doorgen(object):
    '''Дорген'''
    
    def __init__(self):
        '''Инициализация'''
        self.basePath = r'C:\Users\sasch\workspace\doorscenter\src\doorsagents\3rdparty\doorgen'
        self.templatesPath = os.path.join(self.basePath, r'templ')
        self.outPath = os.path.join(self.basePath, r'out\jobs')
        self.textPath = os.path.join(self.basePath, r'text')
        self.snippetsPath = r'C:\Work\snippets'
        self.keywordsFile = os.path.join(self.basePath, r'keys\keywords.txt')
        self.netLinksFile = os.path.join(self.basePath, r'text\netlinks.txt')
        self.pageExtension = '.html'
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
        url = ''
        if keyword != self.keywordDoor:
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
        elif kind == 'A':
            return keyword.title()
        elif kind == 'B':
            return keyword.upper()
        elif kind == 'C':
            return keyword.capitalize()
        else:
            return ''
        
    def _GetFileLines(self, fileName):
        '''Читаем строки из файла'''
        return [item.strip() for item in codecs.open(fileName, encoding='cp1251', errors='ignore').readlines()]
    
    def _GetCachedFileLines(self, fileName):
        '''Читаем и кэшируем строки из файла'''
        if fileName not in self.filesCache:
            self.filesCache[fileName] = ['']
            if os.path.exists(fileName):
                self.filesCache[fileName] = self._GetFileLines(fileName)
        return self.filesCache[fileName]
    
    '''Обработка макросов'''
    
    def GetMainKeyword(self, macrosName, macrosArgsList):
        '''Главный кейворд'''
        keyword = self.keywordDoor
        kind = macrosName.replace('DOORKEYWORD', '')
        return self._Capitalize(keyword, kind)
    
    def GetPageKeyword(self, macrosName, macrosArgsList):
        '''Кейворд страницы'''
        keyword = self.keywordPage
        kind = macrosName.replace('BOSKEYWORD', '')
        return self._Capitalize(keyword, kind)
    
    def GetRandomKeyword(self, macrosName, macrosArgsList):
        '''Случайный кейворд'''
        keyword = random.choice(self.keywordsListFull)
        kind = macrosName.replace('RANDKEYWORD', '')
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
        kind = macrosName.replace('RANDLINK', '')
        return '<a href="%s">%s</a>' % (self._KeywordToUrl(keyword), self._Capitalize(keyword, kind))
    
    def GetRandomNetLink(self, macrosName, macrosArgsList):
        '''Случайная внешний анкор'''
        return random.choice(self.netLinksList)
    
    def GetRandomTextLine(self, macrosName, macrosArgsList):
        '''Случайная строка из файла'''
        fileName = os.path.join(self.textPath, macrosArgsList[0])
        return self.PreprocessTemplate(random.choice(self._GetCachedFileLines(fileName)))
    
    def GetRandomSnippet(self, macrosName, macrosArgsList):
        '''Случайный сниппет'''
        fileName = os.path.join(self.snippetsPath, macrosArgsList[0])
        return self.PreprocessTemplate(random.choice(self._GetCachedFileLines(fileName)))
    
    def GetIndexLink(self, macrosName, macrosArgsList):
        '''Анкор на индекс'''
        if self.keywordPage == self.keywordDoor:
            return ''
        return '<a href="index%s">%s</a>' % (self.pageExtension, self.keywordDoor.title())
        
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
            result += '<a href="%s">%s</a><br/>\n' % (self._KeywordToUrl(keyword), keyword.title())
        return result
    
    def GetDorHost(self, macrosName, macrosArgsList):
        '''Хост дора'''
        return urlparse.urlparse(self.url).hostname
    
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
        template = re.sub(r'{([A-Z0-9_/]*?)}', self.ProcessMacrosRegex, template)
        if template.find('{') < 0:
            return template
        template = re.sub(r'{([A-Z0-9_/]*?)\(([^{},\)]*)\)}', self.ProcessMacrosRegex, template)
        if template.find('{') < 0:
            return template
        template = re.sub(r'{([A-Z0-9_/]*?)\(([^{},\)]*),([^{},\)]*)\)}', self.ProcessMacrosRegex, template)
        '''Процессинг остальных макросов'''
        '''while True:
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
                template = templateBefore + template'''
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
        pageFileName = os.path.join(self.localPath, self._KeywordToUrl(self.keywordPage))
        codecs.open(pageFileName, 'w', encoding='cp1251', errors='ignore').write(pageContents)

    def Generate(self, template, pagesCount, localFolder, url):
        '''Параметры генерации'''
        self.templatePath = os.path.join(self.templatesPath, template)
        self.pagesCount = pagesCount
        self.localPath = os.path.join(self.outPath, localFolder)
        self.url = url
        
        '''Начинаем'''
        dateTimeStart = datetime.datetime.now()
        self.macrosUnknown = set()
        self.filesCache = {}
        self.lastRandomNumber = 0;
        
        '''Очищаем папку дора. Копируем все файлы из шаблона в папку дора, за исключением index.html и dp_sitemap.html'''
        if os.path.exists(self.localPath):
            shutil.rmtree(self.localPath)
        shutil.copytree(self.templatePath, self.localPath)
        for fileName in glob.glob(os.path.join(self.localPath, 'dp_*')):
            os.remove(fileName)
        
        '''Читаем кейворды и ссылки. Обрабатываем кейворды'''
        self.keywordsListFull = self._GetFileLines(self.keywordsFile)
        self.keywordsListShort = self.keywordsListFull[:self.pagesCount]
        self.keywordDoor = self.keywordsListShort[0]
        self.netLinksList = self._GetFileLines(self.netLinksFile)
        
        '''Формируем страницы дора и карту сайта в HTML'''
        indexTemplateContents = self.PreprocessTemplate('\n'.join(self._GetFileLines(os.path.join(self.templatePath, 'index.html'))))
        for keywordPage in self.keywordsListShort:
            self.GeneratePage(indexTemplateContents, keywordPage)
        sitemapTemplateContents = self.PreprocessTemplate('\n'.join(self._GetFileLines(os.path.join(self.templatePath, 'dp_sitemap.html'))))
        self.GeneratePage(sitemapTemplateContents, 'sitemap')
        
        '''Карта сайта в XML'''
        with open(os.path.join(self.localPath, 'sitemap.xml'), 'w') as fd:
            fd.write('''<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n''')
            for keyword in self.keywordsListShort:
                fd.write('''  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.5</priority>\n  </url>\n''' % (self.url + self._KeywordToUrl(keyword), datetime.date.today().strftime('%Y-%m-%d')))
            fd.write('''</urlset>''')
        
        '''Отчет о проделанной работе'''
        if len(self.macrosUnknown) > 0:
            print('Unknown macros (%d): %s.' % (len(self.macrosUnknown), ', '.join(list(self.macrosUnknown))))
        print('Done in %d sec.' % (datetime.datetime.now() - dateTimeStart).seconds)

def Test():
    doorgen = Doorgen()
    doorgen.Generate('mamba-en', 100, 'door8773-new', 'http://lormont.wikidating.info/')

if __name__ == '__main__':
    cProfile.run('Test()')
    #Test()


'''TODO:
1. add_page_key
2. разные даты в карте сайта xml
3. оставлять неизвестные макросы
4. COUNTRAND
'''
