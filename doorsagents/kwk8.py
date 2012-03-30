# coding=utf8
'''
Вся работа происходит в памяти, без промежуточных файлов
python 2.6

Функционал работы со списками кеев и ссылок:
+ число строк
+ базовая чистка, в т.ч. приведение к нижнему регистру
+ сортировка по алфавиту/по длине/по параметру (разные алгоритмы)
+ перемешивание
+ удаление дубликатов (разные алгоритмы, меняется число строк)
+ выборка строк по кейвордам/блэк-листу (разные алгоритмы, меняется число строк)
+ удаление строк по кейвордам/блэк-листу (разные алгоритмы, меняется число строк)
'''

import random, time, re, codecs

class Kwk8:
    '''Базовый класс'''
    def __init__(self, path, verbose=False, encoding='cp1251'):
        '''path - входной файл, isLinks - кеи или ссылки'''
        self.pathOriginal = path  # исходный файл
        self.countOriginal = 0  # число строк в исходном файле
        self.verbose=verbose
        self.lines = []
        self._Load(self.pathOriginal, encoding)
        
    def _Load(self, path, encoding='cp1251'):
        '''Чтение файла'''
        self._Print('Loading file %s...' % path)
        self._TimeStart()
        with codecs.open(path, 'r', encoding, 'ignore') as fd:
            self.lines = fd.readlines()
        self.countOriginal = self.Count()
        self._Print("- %d lines loaded %s" % (self.Count(), self._TimeFinish()))
        return self
        
    def Extend(self, newItems):
        '''Добавляем кеи из другого списка'''
        self.lines.extend(newItems)
        return self
        
    def Save(self, path = '', encoding='cp1251'):
        '''Записывает строки в файл'''
        if path == '':  # если path == '', то записывает в исходный файл
            path = self.pathOriginal
        self._Print('Saving to file %s...' % path)
        self._TimeStart()
        with codecs.open(path, 'w', encoding, 'ignore') as fd:
            fd.writelines(self.lines)
        self._Print("- {0} lines saved {1}".format(self.Count(), self._TimeFinish()))
        return self
    
    def Items(self):
        '''Доступ к кеям'''
        return self.lines
    
    def Count(self):
        '''Число строк'''
        return len(self.lines)
        
    def _Print(self, s):
        '''Выводит строку'''
        if self.verbose:
            print(s)
    
    def _TimeStart(self):
        '''Засекает текущее время'''
        self.timetoken = time.time()
        
    def _TimeFinish(self):
        '''Возвращает сколько времени прошло'''
        return '({0:.2f} sec.)'.format(time.time() - self.timetoken)
        
    def _ProcessLine(self, line):
        '''Ключ строки. Переопределяется в классах-потомках'''
        return line
    
    def _ProcessLineLen(self, line):
        '''Вспомогательная функция, используется при сортировке'''
        return len(self._ProcessLine(line))
        
    def Basic(self, makeLowerCase=False, stripSpaces=False, allowedChars=''):
        '''Базовая чистка кеев'''
        self._Print('Basic processing...')
        self._TimeStart()
        rxStripSpaces = re.compile(r'\s+')
        if allowedChars != '':
            rxAllowedChars = re.compile(r'[^' + re.escape(allowedChars) + ']')
        newLines = []
        for line in self.lines:
            line = line.strip()
            if makeLowerCase:
                line = line.lower()
            if stripSpaces:
                line = rxStripSpaces.sub(' ', line)
            if allowedChars != '':
                line = rxAllowedChars.sub('', line).strip()
            if line != '':
                newLines.append(line + '\n')
        self._Print('- done %s' % self._TimeFinish())
        self.lines = newLines
        return self
    
    def Sort(self, mode = 'alpha'):
        '''Сортировка, mode: (alfa|length)'''
        self._Print('Sorting by {0}...'.format(mode))
        self._TimeStart()
        if mode == 'alpha':
            self.lines.sort(key=self._ProcessLine)
        if mode == 'length':
            self.lines.sort(key=self._ProcessLineLen)
        self._Print('- done %s' % self._TimeFinish())
        return self
    
    def Shuffle(self):
        '''Перемешивание'''
        self._Print('Shuffling...')
        self._TimeStart()
        random.shuffle(self.lines)
        self._Print('- done %s' % self._TimeFinish())
        return self
    
    def Duplicates(self):
        '''Удаление дубликатов'''
        self._Print('Duplicates removing...')
        self._TimeStart()
        hashes = set()
        newLines = []
        for line in self.lines:
            x = self._ProcessLine(line)
            if not x in hashes:
                hashes.add(x)
                newLines.append(line)
        if self.Count() != 0:
            self._Print('- %d lines (%.2f%%) %s' % (len(newLines), len(newLines) * 100.0 / self.Count(), self._TimeFinish()))
        self.lines = newLines
        return self
    
    def SelectByList(self, keysList):
        '''Выборка по кеям из списка'''       
        self._Print('Selecting by keys...')
        self._TimeStart()
        newLines = []
        for line in self.lines:
            x = self._ProcessLine(line)
            for key in keysList:
                if x.find(key) >= 0:
                    newLines.append(line)
                    break
        if self.Count() != 0:
            self._Print('- %d lines (%.2f%%) %s' % (len(newLines), len(newLines) * 100.0 / self.Count(), self._TimeFinish()))
        self.lines = newLines
        return self
    
    def DeleteByList(self, keysList):
        '''Чистка по кеям из списка'''       
        self._Print('Clearing by keys...')
        self._TimeStart()
        newLines = []
        for line in self.lines:
            found = False
            x = self._ProcessLine(line)
            for key in keysList:
                if x.find(key) >= 0:
                    found = True
                    break
            if not found:
                newLines.append(line)
        if self.Count() != 0:
            self._Print('- %d lines (%.2f%%) %s' % (len(newLines), len(newLines) * 100.0 / self.Count(), self._TimeFinish()))
        self.lines = newLines
        return self
    
    def SelectByFile(self, keysFile, encoding='cp1251'):
        '''Выборка по кеям из файла'''
        if keysFile:
            keysList = []
            for line in codecs.open(keysFile, 'r', encoding, 'ignore'):
                keysList.append(self._ProcessLine(line))
            return self.SelectByList(keysList)
        else:
            return self
        
    def DeleteByFile(self, keysFile, encoding='cp1251'):
        '''Чистка по кеям из файла'''
        if keysFile:
            keysList = []
            for line in codecs.open(keysFile, 'r', encoding, 'ignore'):
                keysList.append(self._ProcessLine(line))
            return self.DeleteByList(keysList)
        else:
            return self

class Kwk8Keys(Kwk8):
    def _ProcessLine(self, line):
        return line.strip().lower()

class Kwk8Links(Kwk8):
    def _ProcessLine(self, line):
        '''Возвращает имя хоста вида "subdomain.domain.com/"'''
        line = line.strip().lower()
        if line.startswith('http://'):
            line = line[7:]
        if line.startswith('www.'):
            line = line[4:]
        line, _, _ = line.partition('/')
        return line + '/'

    def _PostProcessLine(self, line):
        '''Пост-обработка ссылки'''
        while line.find('/./') >= 0:
            line = line.replace('/./', '/')
        ''' index.php '''
        featuresList = '''/action=profile;u=
/index.php?action=
/index.php?do=
/index.php?showforum=
/index.php?showtopic=
/index.php?showuser=
/index.php?topic=
/member.php
/memberlist.php
/newreply.php
/posting.php
/profile.php
/showthread.php
/topic.php
/viewthread.php
/viewtopic.php'''.split('\n')
        for feature in featuresList:
            if line.find(feature) >= 0:
                return line[:line.find(feature)] + '/index.php\n'
        ''' forum.php '''
        featuresList = '''/forum.php'''.split('\n')
        for feature in featuresList:
            if line.find(feature) >= 0:
                return line[:line.find(feature)] + '/forum.php\n'
        ''' yabb.pl '''
        featuresList = '''/yabb.pl'''.split('\n')
        for feature in featuresList:
            if line.find(feature) >= 0:
                return line[:line.find(feature)] + '/yabb.pl\n'
        return line
    
    def PostProcessing(self):
        '''Пост-обработка ссылок с фильтрацией'''
        self._Print('Post processing...')
        self._TimeStart()
        newLines = []
        for line in self.lines:
            x = self._ProcessLine(line)
            isGood = True
            level = x.count('.') + 1
            if (level <= 1) or (level >= 4):  # удаляем домены 1 и 4 и более уровней
                isGood = False
            else:
                zone1 = x.split('.')[-1]
                if zone1 in ['cc', 'tk']:  # удаляем фридомены
                    isGood = False
                else:
                    zone2 = x.split('.')[-2]
                    if (level == 3) and (len(zone2) > 3):  # удаляем домены 3-го уровня
                        isGood = False
            if isGood:
                newLines.append(self._PostProcessLine(line))
        if self.Count() != 0:
            self._Print('- %d lines (%.2f%%) %s' % (len(newLines), len(newLines) * 100.0 / self.Count(), self._TimeFinish()))
        self.lines = newLines
        return self
    
def ProcessKeys(inPathKeywords, outPathKeywords, pathStopwords = None):
    '''Стандартная обработка кеев'''
    return Kwk8Keys(inPathKeywords, False).Basic(True).DeleteByFile(pathStopwords).Duplicates().Shuffle().Save(outPathKeywords).Count()

def ProcessLinks(inPathLinks, outPathLinks):
    '''Стандартная обработка ссылок'''
    return Kwk8Links(inPathLinks, False).Basic().Duplicates().Shuffle().Save(outPathLinks).Count()

def ProcessSnippets(inPathKeywords, outPathKeywords, pathStopwords = [], snippetsStopWords = ['http://', '[url', '.ru', '.com', '.html', '.php']):
    '''Стандартная обработка сниппетов'''
    return Kwk8Keys(inPathKeywords, False).DeleteByList(snippetsStopWords).DeleteByList(pathStopwords).Duplicates().Shuffle().Save(outPathKeywords).Count()

if __name__ == '__main__':
    #ProcessKeys('/home/sasch/temp/list/list1.txt', '/home/sasch/temp/list/list1_out1.txt', '/home/sasch/temp/list/list1_stop.txt')
    #ProcessLinks('/home/sasch/temp/list/list1.txt', '/home/sasch/temp/list/list1_out2.txt')
    #ProcessSnippets('/home/sasch/temp/list/text.txt', '/home/sasch/temp/list/text-out.txt', '/home/sasch/temp/list/stopwords.txt')
    Kwk8Links(r'c:\Work\links\LinksList id266a.txt', True).PostProcessing().Save(r'c:\Work\links\LinksList id266b.txt')
    pass
