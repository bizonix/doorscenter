# coding: utf-8

import os, random
from tplentry import *

class TemplateGenerator1(object):
    '''Генератор шаблонов.'''
    
    def __init__(self, code, tplPath):
        '''Пример кода: "xgen1-adult-596".'''
        params = code.split('-')
        if params[0] == 'xgen1':
            self._Generate('/images/' + params[1], params[2], tplPath)
            print('done')
    
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
    
    def _GetPage(self, strTpl, imgPath, imgCount, minEntries, maxEntries):
        '''Генерация страницы'''
        s = ''
        for _ in range(random.randint(minEntries, maxEntries)):
            s += self._GetEntry()
        s = strTpl.replace('{{strEntries}}', s)
        s = s.replace('{{imgPath}}', imgPath)
        s = s.replace('{{imgCount}}', '%s' % imgCount)
        s = s.replace('{{rndColor1}}', self._GetRandomColor())
        s = s.replace('{{rndColor2}}', self._GetRandomColor())
        s = s.replace('{{rndColor3}}', self._GetRandomColor())
        return s
    
    def _Generate(self, imgPath, imgCount, tplPath):
        '''Генерация шаблона: индекс и карта'''
        if not os.path.exists(tplPath):
            os.makedirs(tplPath)
        with open(os.path.join(tplPath, 'index.html'), 'w') as fd:
            fd.write(self._GetPage(strIndex, imgPath, imgCount, 25, 40))
        with open(os.path.join(tplPath, 'dp_sitemap.html'), 'w') as fd:
            fd.write(self._GetPage(strSitemap, imgPath, imgCount, 2, 3))
    
if __name__ == '__main__':
    agent = TemplateGenerator1('xgen1-adult-596', '/home/sasch/public_html/test.home/tplview')
