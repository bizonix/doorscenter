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

import random, time

class Kwk8:
    '''Базовый класс'''
    def __init__(self, path, verbose=True):
        '''path - входной файл, isLinks - кеи или ссылки'''
        self.pathOriginal = path  # исходный файл
        self.countOriginal = 0  # число строк в исходном файле
        self.verbose=verbose
        self.lines = []
        self._Load(self.pathOriginal)
        
    def _Load(self, path):
        '''Чтение файла'''
        self._Print('Loading file %s...' % path)
        self._TimeStart()
        with open(path, 'r') as fd:
            self.lines = fd.readlines()
        self.countOriginal = self.Count()
        print("- %d lines loaded %s" % (self.Count(), self._TimeFinish()))
        return self
        
    def Save(self, path = ''):
        '''Записывает строки в файл'''
        if path == '':  # если path == '', то записывает в исходный файл
            path = self.pathOriginal
        self._Print('Saving to file %s...' % path)
        self._TimeStart()
        with open(path, 'w') as fd:
            fd.writelines(self.lines)
        print("- {0} lines saved {1}".format(self.Count(), self._TimeFinish()))
        return self
    
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
        
    def Basic(self, makeLowerCase=False):
        '''Базовая чистка кеев'''
        self._Print('Basic processing...')
        self._TimeStart()
        if not makeLowerCase:
            self.lines = [x.strip() + '\n' for x in self.lines]
        else:
            self.lines = [x.strip().lower() + '\n' for x in self.lines]
        self._Print('- done %s' % self._TimeFinish())
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
        self._Print('- %d lines (%.2f%%) %s' % (len(newLines), len(newLines) * 100.0 / self.Count(), self._TimeFinish()))
        self.lines = newLines
        return self
    
    def SelectByFile(self, keysFile):
        '''Выборка по кеям из файла'''
        if keysFile:
            keysList = []
            for line in open(keysFile, 'r'):
                keysList.append(line.strip())
            return self.SelectByList(keysList)
        else:
            return self
        
    def DeleteByFile(self, keysFile):
        '''Чистка по кеям из файла'''
        if keysFile:
            keysList = []
            for line in open(keysFile, 'r'):
                keysList.append(line.strip())
            return self.DeleteByList(keysList)
        else:
            return self

class Kwk8Keys(Kwk8):
    def _ProcessLine(self, line):
        return line

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

def ProcessKeys(inPathKeywords, outPathKeywords, pathStopwords = None):
    '''Стандартная обработка кеев'''
    return Kwk8Keys(inPathKeywords, False).Basic(True).DeleteByFile(pathStopwords).Duplicates().Shuffle().Save(outPathKeywords).Count()

def ProcessLinks(inPathLinks, outPathLinks):
    '''Стандартная обработка ссылок'''
    return Kwk8Links(inPathLinks, False).Basic().Duplicates().Shuffle().Save(outPathLinks).Count()

def Test():
    ProcessKeys('/home/sasch/temp/list/list1.txt', '/home/sasch/temp/list/list1_out1.txt', '/home/sasch/temp/list/list1_stop.txt')
    ProcessLinks('/home/sasch/temp/list/list1.txt', '/home/sasch/temp/list/list1_out2.txt')

if __name__ == '__main__':
    Test()
