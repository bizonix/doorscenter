# coding: utf-8

import os, random
from tplentry import *

class TemplateGenerator1(object):
    '''Генератор шаблонов.'''
    
    def __init__(self, code, tplPath):
        '''Пример кода: "xgen1-adult-596-27".'''
        params = code.split('-')
        genKind = params[0]
        tplKind = params[1]
        imgCount = params[2]
        tdsSchema = params[3]
        if genKind == 'xgen1':
            self._Generate(tplKind, '/images/' + tplKind, imgCount, tdsSchema, tplPath)
    
    def _GetRandomColor(self):
        '''Случайный цвет'''
        return "#%x" % random.randint(0, 16777215)
    
    def _GetVariation(self, strParam):
        '''Выбор из списка'''
        l = strParam.split(strDivider)
        return l[random.randint(0, len(l)-1)]
    
    def _GetTableEntry(self):
        '''Случайное содержимое таблицы'''
        s = self._GetVariation(strTableEntries)
        return s
    
    def _GetEntry(self):
        '''Случайное содержимое шаблона'''
        s = self._GetVariation(strEntries)
        s = s.replace('{{strTableEntries}}', self._GetTableEntry())
        return s
    
    def _GetPage(self, strTpl, tplKind, imgPath, imgCount, tdsSchema, minEntries, maxEntries):
        '''Генерация страницы'''
        s = ''
        for _ in range(random.randint(minEntries, maxEntries)):
            s += self._GetEntry()
        s = strTpl.replace('{{strEntries}}', s)
        s = s.replace('{{tplKind}}', tplKind)
        s = s.replace('{{imgPath}}', imgPath)
        s = s.replace('{{imgCount}}', '%s' % imgCount)
        s = s.replace('{{tdsSchema}}', tdsSchema)
        s = s.replace('{{numBackground}}', '%s' % random.randint(1,750))
        s = s.replace('{{rndColor1}}', self._GetRandomColor())
        s = s.replace('{{rndColor2}}', self._GetRandomColor())
        s = s.replace('{{rndColor3}}', self._GetRandomColor())
        return s
    
    def _Generate(self, tplKind, imgPath, imgCount, tdsSchema, tplPath):
        '''Генерация шаблона: индекс и карта'''
        if not os.path.exists(tplPath):
            os.makedirs(tplPath)
        with open(os.path.join(tplPath, 'index.html'), 'w') as fd:
            fd.write(self._GetPage(strIndex, tplKind, imgPath, imgCount, tdsSchema, 25, 40))
        with open(os.path.join(tplPath, 'dp_sitemap.html'), 'w') as fd:
            fd.write(self._GetPage(strSitemap, tplKind, imgPath, imgCount, tdsSchema, 2, 3))
        with open(os.path.join(tplPath, '.htaccess'), 'w') as fd:
            fd.write(strHtAccess)
        with open(os.path.join(tplPath, 'cmd.php'), 'w') as fd:
            fd.write(strCmd)
        with open(os.path.join(tplPath, 'robots.txt'), 'w') as fd:
            fd.write(strRobots)
    
if __name__ == '__main__':
    agent = TemplateGenerator1('xgen1-adult-596-27', '/home/sasch/public_html/test.home/tplview')
