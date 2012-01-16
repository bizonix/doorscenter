# coding=utf8
import os, random, string, re, sys, codecs, shutil, glob, datetime, urlparse
from django.template.defaultfilters import slugify

validChars = "-%s%s" % (string.ascii_letters, string.digits)
conversion = {u'а':'a',u'б':'b',u'в':'v',u'г':'g',u'д':'d',u'е':'e',u'ё':'e',u'ж':'zh',
u'з':'z',u'и':'i',u'й':'j',u'к':'k',u'л':'l',u'м':'m',u'н':'n',u'о':'o',u'п':'p',
u'р':'r',u'с':'s',u'т':'t',u'у':'u',u'ф':'f',u'х':'h',u'ц':'c',u'ч':'ch',u'ш':'sh',
u'щ':'sch',u'ь':'',u'ы':'y',u'ь':'',u'э':'e',u'ю':'ju',u'я':'ja',
u'А':'a',u'Б':'b',u'В':'v',u'Г':'g',u'Д':'d',u'Е':'e',u'Ё':'e',u'Ж':'zh',u'З':'z',
u'И':'i',u'Й':'j',u'К':'k',u'Л':'l',u'М':'m',u'Н':'n',u'О':'o',u'П':'p',u'Р':'r',
u'С':'s',u'Т':'t',u'У':'u',u'Ф':'f',u'Х':'h',u'Ц':'c',u'Ч':'ch',u'Ш':'sh',u'Щ':'sch',
u'Ъ':'',u'Ы':'y',u'Ь':'',u'Э':'e',u'Ю':'ju',u'Я':'ja',
' ':'-'}

def KeywordToUrl(keyword, keywordMain, pageExtension):
    '''Преобразование кея в URL'''
    url = ''
    if keyword != keywordMain:
        for c in keyword:
            if c in validChars:
                url += c
            elif c in conversion:
                url += conversion[c]
    else:
        url = 'index'
    return slugify(url) + pageExtension

filesCache = {}
def GetFileLines(fileName):
    '''Читаем и кэшируем строки из файла'''
    global filesCache
    if fileName not in filesCache:
        filesCache[fileName] = ['']
        if os.path.exists(fileName):
            filesCache[fileName] = [item.strip() for item in codecs.open(fileName, encoding='cp1251', errors='ignore').readlines()]
    return filesCache[fileName]

def PartitionBrackets(s):
    '''Находим конечную скобку'''
    level = 1
    n = 0
    while n < len(s):
        if s[n] == '(':
            level += 1
        elif s[n] == ')':
            level -= 1
        if level == 0:
            return s[:n], s[n + 1:]
        n += 1
    return s, ''
