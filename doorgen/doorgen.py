# coding=utf8
import os, random, string, re, sys, codecs, shutil, glob, datetime, urlparse
from common import FindMacros
from django.template.defaultfilters import slugify

class Pagegen(object):
    '''Генератор страницы дора'''
    
    def __init__(self, doorgen, contents):
        '''Инициализация'''
        self.doorgen = doorgen
        self.contents = contents
        self.validChars = "-%s%s" % (string.ascii_letters, string.digits)
        self.conversion = {u'а':'a',u'б':'b',u'в':'v',u'г':'g',u'д':'d',u'е':'e',u'ё':'e',u'ж':'zh',
        u'з':'z',u'и':'i',u'й':'j',u'к':'k',u'л':'l',u'м':'m',u'н':'n',u'о':'o',u'п':'p',
        u'р':'r',u'с':'s',u'т':'t',u'у':'u',u'ф':'f',u'х':'h',u'ц':'c',u'ч':'ch',u'ш':'sh',
        u'щ':'sch',u'ь':'',u'ы':'y',u'ь':'',u'э':'e',u'ю':'ju',u'я':'ja',
        u'А':'a',u'Б':'b',u'В':'v',u'Г':'g',u'Д':'d',u'Е':'e',u'Ё':'e',u'Ж':'zh',u'З':'z',
        u'И':'i',u'Й':'j',u'К':'k',u'Л':'l',u'М':'m',u'Н':'n',u'О':'o',u'П':'p',u'Р':'r',
        u'С':'s',u'Т':'t',u'У':'u',u'Ф':'f',u'Х':'h',u'Ц':'c',u'Ч':'ch',u'Ш':'sh',u'Щ':'sch',
        u'Ъ':'',u'Ы':'y',u'Ь':'',u'Э':'e',u'Ю':'ju',u'Я':'ja',
        ' ':'-'}
    
    def _KeywordToUrl(self, keyword):
        '''Преобразование кея в URL'''
        url = ''
        if keyword != self.keywordMain:
            for c in keyword:
                if c in self.validChars:
                    url += c
                elif c in self.conversion:
                    url += self.conversion[c]
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
        
    '''Обработка макросов'''
    
    def GetMainKeyword(self, macrosName, macrosArgsList, after):
        '''Главный кейворд'''
        keyword = self.keywordMain
        kind = macrosName.replace('BOSKEYWORD', '').replace('KEYWORD', '')
        return self._Capitalize(keyword, kind), after
    
    def GetPageKeyword(self, macrosName, macrosArgsList, after):
        '''Кейворд страницы'''
        keyword = self.keywordPage
        kind = macrosName.replace('BOSKEYWORD', '').replace('KEYWORD', '')
        return self._Capitalize(keyword, kind), after
    
    def GetRandomKeyword(self, macrosName, macrosArgsList, after):
        '''Случайный кейворд'''
        keyword = random.choice(self.keywordsListFull)
        kind = macrosName.replace('RANDKEYWORD', '').replace('RAND_KEY', '')
        return self._Capitalize(keyword, kind), after
    
    def GetRandomNumber(self, macrosName, macrosArgsList, after):
        '''Случайное число'''
        return str(random.randint(int(macrosArgsList[0]), int(macrosArgsList[1]))), after
    
    def GetRandomIntLinkUrl(self, macrosName, macrosArgsList, after):
        '''Случайный внутренний короткий урл'''
        keyword = random.choice(self.keywordsListFull)
        return self._KeywordToUrl(keyword), after
    
    def GetRandomIntLink(self, macrosName, macrosArgsList, after):
        '''Случайный внутренний анкор'''
        keyword = random.choice(self.keywordsListFull)
        kind = macrosName.replace('RANDLINK', '').replace('RAND_ANCOR', '')
        return '<a href="%s">%s</a>' % (self._KeywordToUrl(keyword), self._Capitalize(keyword, kind)), after
    
    def GetRandomNetLink(self, macrosName, macrosArgsList, after):
        '''Случайная внешний анкор'''
        return random.choice(self.netLinksList), after
    
    def GetRandomTextLine(self, macrosName, macrosArgsList, after):
        '''Случайная строка из файла'''
        fileName = os.path.join(self.textPath, macrosArgsList[0])
        return random.choice(self._GetFileLines(fileName)), after
    
    def GetRandomSnippet(self, macrosName, macrosArgsList, after):
        '''Случайный сниппет'''
        fileName = os.path.join(self.snippetsPath, macrosArgsList[0])
        return random.choice(self._GetFileLines(fileName)), after
    
    def GetIndexLink(self, macrosName, macrosArgsList, after):
        '''Анкор на индекс'''
        if self.keywordPage != self.keywordMain:
            return '<a href="index%s">%s</a>' % (self.pageExtension, self.keywordMain.title()), after
        else:
            return '', after
        
    def GetSitemapLink(self, macrosName, macrosArgsList, after):
        '''Анкор на карту сайта'''
        if self.keywordPage == self.keywordMain:
            return '<a href="sitemap%s">Sitemap</a>' % self.pageExtension, after
        else:
            return '', after
    
    def GetSitemapLinks(self, macrosName, macrosArgsList, after):
        '''Анкоры на все страницы дора для карты сайта'''
        if self.keywordPage == 'sitemap':
            s = ''
            for keyword in self.keywordsListShort:
                s += '<a href="%s">%s</a><br/>\n' % (self._KeywordToUrl(keyword), keyword.title())
            return s, after
        else:
            return '', after
    
    def GetDorHost(self, macrosName, macrosArgsList, after):
        '''Хост дора'''
        return urlparse.urlparse(self.url).hostname, after
    
    def ProcessCycle(self, macrosName, macrosArgsList, after):
        '''Обрабатываем цикл'''
        macrosEnd = '{' + macrosName.replace('FOR', 'ENDFOR') + '}'
        macrosCounter = '{I' + macrosName.replace('FOR', '') + '}'
        body, _, after = after.partition(macrosEnd)
        contents = ''
        for counter in range(int(macrosArgsList[0]), int(macrosArgsList[1]) + 1):
            contents += self.ProcessContents(body.replace(macrosCounter, str(counter)))
        return contents, after
    

    '''Обработка страницы'''
    
    def ProcessContents(self, contents):
        '''Заменяем макросы на странице'''
        macrosDict = {'BOSKEYWORD':self.GetPageKeyword, 'ABOSKEYWORD':self.GetPageKeyword, 'BBOSKEYWORD':self.GetPageKeyword, 'CBOSKEYWORD':self.GetPageKeyword, 
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
        while True:
            before, macrosName, macrosArgsList, after = FindMacros(contents)
            macrosArgsList = [self.ProcessContents(item) for item in macrosArgsList]
            if macrosName == '':
                break
            elif macrosName in macrosDict:
                x, after = macrosDict[macrosName](macrosName, macrosArgsList, after)
                contents = before + self.ProcessContents(x) + after
                contents = before + x + after
            else:
                self.macrosUnknown.add(macrosName)
                contents = before + after
        return contents
    
    def Generate(self, keywordPage):
        '''Формируем страницу'''
        self.keywordPage = keywordPage
        pageContents = self.ProcessContents(self.contents)
        pageFileName = os.path.join(self.localPath, self._KeywordToUrl(self.keywordPage))
        codecs.open(pageFileName, 'w', encoding='cp1251', errors='ignore').write(pageContents)


class Doorgen(object):
    '''Дорген'''
    
    def __init__(self):
        '''Инициализация'''
        self.basePath = r'C:\Users\sasch\workspace\doorscenter\src\doorsagents\3rdparty\doorgen'
        self.textPath = os.path.join(self.basePath, r'text')
        self.snippetsPath = r'C:/Work/snippets'
        self.keywordsFile = os.path.join(self.basePath, r'keys\keywords.txt')
        self.netLinksFile = os.path.join(self.basePath, r'text\netlinks.txt')
        self.pageExtension = '.html'
        self.filesCache = {}

    def _GetFileLines(self, fileName):
        '''Читаем и кэшируем строки из файла'''
        if fileName not in self.filesCache:
            self.filesCache[fileName] = ['']
            if os.path.exists(fileName):
                self.filesCache[fileName] = [item.strip() for item in codecs.open(fileName, encoding='cp1251', errors='ignore').readlines()]
        return self.filesCache[fileName]
    
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
        indexContents = codecs.open(os.path.join(self.templatePath, 'index.html'), encoding='cp1251', errors='ignore').read()
        pagegen = Pagegen(self, indexContents)
        for keywordPage in self.keywordsListShort:
            pagegen.Generate(keywordPage)
        #sitemapContents = codecs.open(os.path.join(self.templatePath, 'dp_sitemap.html'), encoding='cp1251', errors='ignore').read()
        #self.keywordPage = 'sitemap'
        #self.ProcessPage(sitemapContents)
        
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
