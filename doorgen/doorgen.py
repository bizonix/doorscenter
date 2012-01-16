# coding=utf8
import os, random, string, re, sys, codecs, shutil, glob, datetime, urlparse
from common import KeywordToUrl, GetFileLines, PartitionBrackets

'''Обработка макросов'''

def Capitalize(keyword, kind):
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
    
def GetMainKeyword(m):
    '''Главный кейворд'''
    return Capitalize(keywordMain, m.group(1))

def GetRandomKeyword(m):
    '''Случайный кейворд'''
    return Capitalize(random.choice(keywordsList), m.group(1))

def GetRandomNumber(m):
    '''Случайное число'''
    return str(random.randint(int(m.group(1)), int(m.group(2))))

def GetRandomIntLinkUrl(m):
    '''Случайный внутренний короткий урл'''
    keyword = random.choice(keywordsList)
    return KeywordToUrl(keyword, keywordMain, pageExtension)

def GetRandomIntLink(m):
    '''Случайный внутренний анкор'''
    keyword = random.choice(keywordsList)
    return '<a href="%s">%s</a>' % (KeywordToUrl(keyword, keywordMain, pageExtension), Capitalize(keyword, m.group(1)))

def GetRandomNetLink(m):
    '''Случайная внешний анкор'''
    return random.choice(netLinksList)

def GetIndexLink(m):
    '''Анкор на индекс'''
    return '<a href="index%s">%s</a>' % (pageExtension, keywordMain.title())
    
def GetSitemapLink(m):
    '''Анкор на карту сайта'''
    return '<a href="sitemap%s">Sitemap</a>' % pageExtension

def GetRandomTextLine(m):
    '''Случайная строка из файла'''
    fileName = os.path.join(textPath, m.group(1))
    return random.choice(GetFileLines(fileName))

def GetRandomSnippet(m):
    '''Случайный сниппет'''
    fileName = os.path.join(snippetsPath, m.group(1))
    return random.choice(GetFileLines(fileName))

def GetSitemapLinks(m):
    '''Анкоры на все страницы дора для карты сайта'''
    s = ''
    for keyword in keywordsList[:pagesCount]:
        s += '<a href="%s">%s</a><br/>\n' % (KeywordToUrl(keyword, keywordMain, pageExtension), keyword.title())
    return s

def GetDorHost(m):
    '''Хост дора'''
    return urlparse.urlparse(url).hostname

def ProcessCycle(contents, keyword, cycleStartToken, cycleEndToken, cycleNumberToken):
    '''Делим цикл на части'''
    before, _, x = contents.partition(cycleStartToken)
    inside, x = PartitionBrackets(x)
    counterFrom, _, counterTo = ProcessContents(inside, keyword).partition(',')
    body, _, after = x[1:].partition(cycleEndToken)
    '''Обрабатываем цикл'''
    contents = ProcessContents(before, keyword)
    counter = int(counterFrom)
    while counter <= int(counterTo):
        contents += ProcessContents(body.replace(cycleNumberToken, str(counter)), keyword)
        counter += 1
    contents += ProcessContents(after, keyword)
    return contents

def ProcessUnknownMacros(m):
    '''Запоминаем неизвестные макросы'''
    global macrosUnknown
    macros = m.group(1)
    if macros.find(':') >= 0:  # CSS
        return '{' + macros + '}'
    else:
        if macros != 'PIWIK':
            macrosUnknown.add(macros)
        return ''


'''Обработка страницы'''

def ProcessContents(contents, keyword):
    '''Заменяем макросы на странице'''
    '''Находим циклы'''
    if contents.find('{FORX(') >= 0:
        contents = ProcessCycle(contents, keyword, '{FORX(', '{ENDFORX}', '{IX}')
    elif contents.find('{FOR(') >= 0:
        contents = ProcessCycle(contents, keyword, '{FOR(', '{ENDFOR}', '{I}')
    else:
        '''Заменяем прочие макросы'''
        contents = re.sub(r'{([A|B|C]?)BOSKEYWORD}', GetMainKeyword, contents)
        contents = re.sub(r'{([B|BB]?)KEYWORD}', GetMainKeyword, contents)
        contents = re.sub(r'{([A|B|C]?)RANDKEYWORD}', GetRandomKeyword, contents)
        contents = re.sub(r'{([B|BB]?)RAND_KEY}', GetRandomKeyword, contents)
        contents = re.sub(r'{([A|B|C]?)RANDLINK}', GetRandomIntLink, contents)
        contents = re.sub(r'{([B|BB]?)RAND_ANCOR}', GetRandomIntLink, contents)
        contents = re.sub(r'{RAND_URL}', GetRandomIntLinkUrl, contents)
        contents = re.sub(r'{RANDLINKURL}', GetRandomIntLinkUrl, contents)
        contents = re.sub(r'{RANDMYLINK}', GetRandomNetLink, contents)
        contents = re.sub(r'{RAND\(([^,)]*?),([^))]*?)\)}', GetRandomNumber, contents)
        contents = re.sub(r'{RANDTEXTLINE\(([^\)]*?)\)}', GetRandomTextLine, contents)
        contents = re.sub(r'{SNIPPET\(([^\)]*?)\)}', GetRandomSnippet, contents)
        contents = re.sub(r'{DOR_HOST}', GetDorHost, contents)
        
        '''Макросы, специфические для разных видов страниц'''
        if keyword == keywordMain:  # главная
            contents = re.sub(r'{INDEX}', '', contents)
            contents = re.sub(r'{INDEXLINK}', '', contents)
            contents = re.sub(r'{SITEMAPLINK}', GetSitemapLink, contents)
            contents = re.sub(r'{MAPS_ }', GetSitemapLink, contents)
            contents = re.sub(r'{ALLLINK}', '', contents)
            contents = re.sub(r'{MAP_LINKS_ }', '', contents)
        elif keyword == 'sitemap':  # карта сайта
            contents = re.sub(r'{INDEX}', GetIndexLink, contents)
            contents = re.sub(r'{INDEXLINK}', GetIndexLink, contents)
            contents = re.sub(r'{SITEMAPLINK}', '', contents)
            contents = re.sub(r'{MAPS_ }', '', contents)
            contents = re.sub(r'{ALLLINK}', GetSitemapLinks, contents)
            contents = re.sub(r'{MAP_LINKS_ }', GetSitemapLinks, contents)
        else:  # остальные страницы
            contents = re.sub(r'{INDEX}', GetIndexLink, contents)
            contents = re.sub(r'{INDEXLINK}', GetIndexLink, contents)
            contents = re.sub(r'{SITEMAPLINK}', '', contents)
            contents = re.sub(r'{MAPS_ }', '', contents)
            contents = re.sub(r'{ALLLINK}', '', contents)
            contents = re.sub(r'{MAP_LINKS_ }', '', contents)
        
        '''Неизвестные макросы'''
        contents = re.sub(r'{([^}]*?)}', ProcessUnknownMacros, contents)
    return contents

def ProcessPage(contents, keyword):
    '''Формируем страницу'''
    pageContents = ProcessContents(contents, keyword)
    pageFileName = os.path.join(doorgenPath, localPath, KeywordToUrl(keyword, keywordMain, pageExtension))
    codecs.open(pageFileName, 'w', encoding='cp1251', errors='ignore').write(pageContents)


'''Настройки'''
doorgenPath = r'C:\Users\sasch\workspace\doorscenter\src\doorsagents\3rdparty\doorgen'
textPath = os.path.join(doorgenPath, r'text')
snippetsPath = r'C:/Work/snippets'
keywordsFile = os.path.join(doorgenPath, r'keys\keywords.txt')
netLinksFile = os.path.join(doorgenPath, r'text\netlinks.txt')
pageExtension = '.html'

'''Параметры генерации'''
templatePath = r'templ\mamba-en'
pagesCount = 100
localPath = r'out\jobs\door8773-new'
url = 'http://lormont.wikidating.info/'

'''Генерируем дор'''
dateTimeStart = datetime.datetime.now()
macrosUnknown = set()

'''Очищаем папку дора. Копируем все файлы из шаблона в папку дора, за исключением index.html и dp_sitemap.html'''
if os.path.exists(os.path.join(doorgenPath, localPath)):
    shutil.rmtree(os.path.join(doorgenPath, localPath))
shutil.copytree(os.path.join(doorgenPath, templatePath), os.path.join(doorgenPath, localPath))
for fileName in glob.glob(os.path.join(doorgenPath, localPath, 'dp_*')):
    os.remove(fileName)

'''Читаем кейворды и ссылки. Обрабатываем кейворды'''
keywordsList = [item.strip() for item in codecs.open(keywordsFile, encoding='cp1251', errors='ignore').readlines()]
keywordMain = keywordsList[0]
netLinksList = [item.strip() for item in codecs.open(netLinksFile, encoding='cp1251', errors='ignore').readlines()]

'''Формируем страницы дора и карту сайта в HTML'''
indexContents = codecs.open(os.path.join(doorgenPath, templatePath, 'index.html'), encoding='cp1251', errors='ignore').read()
for keywordPage in keywordsList[:pagesCount]:
    ProcessPage(indexContents, keywordPage)
sitemapContents = codecs.open(os.path.join(doorgenPath, templatePath, 'dp_sitemap.html'), encoding='cp1251', errors='ignore').read()
ProcessPage(sitemapContents, 'sitemap')

'''Карта сайта в XML'''
with open(os.path.join(doorgenPath, localPath, 'sitemap.xml'), 'w') as fd:
    fd.write('''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
''')
    for keyword in keywordsList[:pagesCount]:
        fd.write('''   <url>
      <loc>%s</loc>
      <lastmod>%s</lastmod>
      <changefreq>weekly</changefreq>
      <priority>0.5</priority>
   </url>\n''' % (url + KeywordToUrl(keyword, keywordMain, pageExtension), datetime.date.today().strftime('%Y-%m-%d')))
    fd.write('''</urlset>''')

'''Отчет о проделанной работе'''
if len(macrosUnknown) > 0:
    print('Unknown macros: %s.' % ', '.join(list(macrosUnknown)))
print('Done in %d sec.' % (datetime.datetime.now() - dateTimeStart).seconds)

'''TODO:
1. add_page_key
2. STAT
'''
