# coding=utf8
from django.template.defaultfilters import slugify
import os, glob, math, random, urllib, string, codecs

def AddDomainToControlPanel(domainName, controlPanelType, controlPanelUrl):
    '''Добавить домен в панель управления'''
    if controlPanelType == 'ispconfig':
        try:
            data = {'domainName': domainName, 'controlPanelUrl': controlPanelUrl}
            fd = urllib.urlopen(r'http://searchpro.name/tools/isp-add-domain.php', urllib.urlencode(data))
            reply = fd.read()
            fd.close()
            if reply == 'ok':
                return ''
            else:
                return 'unknown error'
        except Exception as error:
            return str(error)
    else:
        return ''

def SelectKeywords(path, encoding='utf-8', count=10):
    ''' Создание списка кеев для доров по Бабулеру.
    Для каждого дора из каждого файла в папке берется заданный процент кеев.'''
    percentsTotal = 0
    inKeysList = []
    '''Читаем файлы'''
    for file in glob.glob(os.path.join(path, r'[*.txt')):
        _, _, x = file.partition('[')
        x, _, _ = x.partition(']')
        percent = int(x)
        percentsTotal += percent
        tempkeys = []
        for line in codecs.open(file, 'r', encoding):
            tempkeys.append(line.strip())
        inKeysList.append((tempkeys, percent))
    '''Генерируем список'''
    outKeysList = []
    percentsCount = percentsTotal
    for keys, percent in inKeysList:
        keysCount = int(min(len(keys), math.floor(count * percent / percentsCount * random.randint(80, 120) / 100)))  # берем случайное количество кеев из очередного файла 
        if keysCount > 0:
            random.shuffle(keys)  # перемешиваем
            outKeysList.extend(keys[0:keysCount])  # добавляем в результирующий список
        count -= keysCount
        percentsCount -= percent
    '''Перемешиваем'''
    random.shuffle(outKeysList)
    return outKeysList

validChars = "-%s%s" % (string.ascii_letters, string.digits)
conversion = {u'а':'a',u'б':'b',u'в':'v',u'г':'g',u'д':'d',u'е':'e',u'ё':'e',u'ж':'zh',
u'з':'z',u'и':'i',u'й':'j',u'к':'k',u'л':'l',u'м':'m',u'н':'n',u'о':'o',u'п':'p',
u'р':'r',u'с':'s',u'т':'t',u'у':'u',u'ф':'f',u'х':'h',u'ц':'c',u'ч':'ch',u'ш':'sh',
u'щ':'sch',u'ь' : '',u'ы':'y',u'ь' : '',u'э':'e',u'ю':'ju',u'я':'ja',
u'А':'a',u'Б':'b',u'В':'v',u'Г':'g',u'Д':'d',u'Е':'e',u'Ё':'e',u'Ж':'zh',u'З':'z',
u'И':'i',u'Й':'j',u'К':'k',u'Л':'l',u'М':'m',u'Н':'n',u'О':'o',u'П':'p',u'Р':'r',
u'С':'s',u'Т':'t',u'У':'u',u'Ф':'f',u'Х':'h',u'Ц':'c',u'Ч':'ch',u'Ш':'sh',u'Щ':'sch',
u'Ъ' : '',u'Ы':'y',u'Ь' : '',u'Э':'e',u'Ю':'ju',u'Я':'ja'}

def KeywordToUrl(key):
    '''Преобразование кея в разрешенные символы URL'''
    url = ''
    for c in key:
        if c in validChars:
            url += c
        elif c in conversion:
            url += conversion[c]
    return slugify(url)        

def GetFirstObject(objects):
    '''Первый ненулевой объект из списка'''
    for object in objects:
        if object:
            return object
    return None
