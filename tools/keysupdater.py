# coding=utf8
import os, sys, glob, datetime, operator, string, MySQLdb, kwk8

''' Автоматический апдейт кейвордов

I. Получение кейвордов.

1. Получаем кейворды с TDS. На входе - номера схем, на выходе - файл в заданной папке.
2. (По желанию) В ту же папку помещаются вручную полученные кейворды.

II. Обработка и апдейт кейвордов.

1. Кейводры из всех файлов в рабочей папке смешиваются.
2. Удаление дублей и чистка по блэк-листу.
3. (По желанию) Фильтрация по адалт-листу.
4. Базовая чистка: оставляем только разрешенные символы [a-z ] и удаляем лишние пробелы.
5. Из целевой папки читаются кейворды файлов и сортируются по их весу.
6. Цикл по кейвордам файлов:
6.1. Выборка из новых кейвордов по кейворду файла.
6.2. Удаление по предыдущим кейвордам файлов.
6.2. Апдейт файла с удалением дублей.

'''

class KeywordsGetter(object):
    '''Получение кейвордов'''
    
    def __init__(self, folderName):
        '''Инициализация'''
        self.folderName = folderName
        
    def _GetFileName(self, code, sourceType):
        '''Формируем имя файла'''
        return os.path.join(self.folderName, '%s-%s.txt' % (code, sourceType))
        
    def GetFromTDS(self, schemesList, code, limit = 0):
        '''Получение кейвордов с TDS по номерам схем'''
        print('Getting new keywords from TDS ...')
        dateTimeStart = datetime.datetime.now()
        schemesList = [str(item) for item in schemesList]
        sql = 'select distinct `query` from `stats` where `sid` in (' + ','.join(schemesList) + ')'
        if limit > 0:
            sql += ' limit 0, %d' % limit
        try:
            db = MySQLdb.connect('searchpro.name', 'tds', 'T34c1r1M', 'tds')
            try:
                cursor = db.cursor()
                try:
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    keywords = [item[0].strip().lower() for item in results if item[0].strip() != '']
                    print('Keywords got: %d' % len(keywords))
                    open(self._GetFileName(code, 'tds'), 'w').write('\n'.join(keywords))
                except Exception as error:
                    print('Error: %s' % error)
                cursor.close()
            except Exception as error:
                print('Error: %s' % error)
            db.close()
        except Exception as error:
            print('Error: %s' % error)
        print('Done in %d sec.' % ((datetime.datetime.now() - dateTimeStart).seconds))

class KeywordsUpdater(object):
    '''Апдейт набора кейвордов'''
    
    def __init__(self, updateKeywordsFolder, listKeywordsFolder, newKeywordsFolder, code):
        '''Инициализация'''
        self.updateKeywordsFolder = updateKeywordsFolder
        self.listKeywordsFolder = listKeywordsFolder
        self.newKeywordsFolder = newKeywordsFolder
        self.code = code
        self.tempFileName = os.path.join(self.newKeywordsFolder, '%s-temp.txt' % self.code)
        self.blackListFileName = os.path.join(self.listKeywordsFolder, 'black-list.txt')
        self.whiteListFileName = os.path.join(self.listKeywordsFolder, 'white-list.txt')
        
    def Update(self):
        '''Непосредственно апдейт'''
        '''Объединяем кейворды из папки с новыми кейвордами'''
        print('Joining new keywords ...')
        dateTimeStart = datetime.datetime.now()
        newKeywords = []
        for fileName in glob.glob(os.path.join(self.newKeywordsFolder, '%s-*.txt' % self.code)):
            if fileName != self.tempFileName:
                newKeywords.extend(open(fileName).readlines())
        open(self.tempFileName, 'w').writelines(newKeywords)
        
        '''Чистим новые кейворды по черному и белому спискам'''
        validChars = "%s%s " % (string.ascii_letters, string.digits)
        kwk = kwk8.Kwk8Keys(self.tempFileName).Basic(True, True).Duplicates()
        print('New keywords count: %d' % kwk.Count())
        if os.path.exists(self.blackListFileName):
            kwk.DeleteByFile(self.blackListFileName)
            print('New keywords count after black list: %d' % kwk.Count())
        if os.path.exists(self.whiteListFileName):
            kwk.SelectByFile(self.whiteListFileName)
            print('New keywords count after white list: %d' % kwk.Count())
        kwk.Basic(True, True, validChars).Duplicates().Save()
        
        '''Читаем главные кейворды из основной папки и сортируем их по приоритету.
        Получаем отсортированный список кортежей из кейворда и имени файла'''
        mainKeywords = sorted(glob.glob(os.path.join(self.updateKeywordsFolder, '[*.txt')), reverse = True)  # находим файлы и сортируем их
        mainKeywords = [(os.path.basename(item).replace('.txt', ''), item) for item in mainKeywords]  # убираем путь и расширение
        mainKeywords = [(item[0][item[0].find(']') + 1:], item[1]) for item in mainKeywords]  # убираем вес
        joinKeywords = [(item[0], item[1]) for item in mainKeywords if item[0].find('join') == 0]  # находим файл с "прочими" кейвордами
        mainKeywords = [(item[0], item[1]) for item in mainKeywords if item[0].find('join') < 0]  # удаляем из списка главных кейвордов файл с "прочими" кейвордами
        
        '''Апдейт файлов с главными кейвордами'''
        processedKeywords = []
        for mainKeyword, mainKeywordFileName in mainKeywords:
            kwkMain = kwk8.Kwk8Keys(mainKeywordFileName)
            mainCountOld = kwkMain.Count()
            kwkNew = kwk8.Kwk8Keys(self.tempFileName).SelectByList([mainKeyword]).DeleteByList(processedKeywords)
            mainCountNew = kwkMain.Extend(kwkNew.Items()).Duplicates().Save().Count()
            print('- %s: %d added' % (mainKeyword, mainCountNew - mainCountOld))
            processedKeywords.append(mainKeyword)
        
        '''Обрабатываем оставшиеся кейворды'''
        if len(joinKeywords) > 0:
            joinKeywordsFileName = joinKeywords[0][1]
            kwkJoin = kwk8.Kwk8Keys(joinKeywordsFileName)
            joinCountOld = kwkJoin.Count()
            kwkNew = kwk8.Kwk8Keys(self.tempFileName).DeleteByList(processedKeywords)
            joinCountNew = kwkJoin.Extend(kwkNew.Items()).Duplicates().Save().Count()
            print('- join: %d added' % (joinCountNew - joinCountOld))
        
        '''Результаты'''
        os.unlink(self.tempFileName)
        print('Done in %d sec.' % ((datetime.datetime.now() - dateTimeStart).seconds))
        
if __name__ == '__main__':
    #KeywordsGetter(r'c:\Temp\7').GetFromTDS([17, 43], 'dating')
    KeywordsUpdater(r'c:\Users\sasch\workspace\doorscenter\src\doorsadmin\keywords\adult-chat', r'c:\Users\sasch\workspace\doorscenter\src\doorsadmin\keywords', r'c:\Temp\7', 'dating').Update()


''' Этапы парсинга:

I. Постановка задачи.
I.1. Определяем главный кейворд.
I.2. Придумываем и находим в облаках смежные кейворды.
I.3. Сортируем их в порядке приоритета.

II. Выборка (выполняется последовательно для каждого кейворда из предыдущего пункта).
II.1. Делаем выборку из Пастухова, базы 60, 77, 245, без модификаторов.
II.2. Находим словоформы кейворда (см. скрипт ниже).
II.3. Делаем выборку из Пастухова по всем словоформам с модификатором '[]'.
II.4. Делаем выборку из ActualKeywords по всем словоформам без модификаторов.
iI.5. Делаем выборку из piwik: "SELECT distinct `referer_keyword` FROM `piwik_log_visit` WHERE `referer_keyword` like '%chat%'".  !!! доработать
II.6. Делаем выборку из tds: "SELECT distinct `query` FROM `stats` where `query` like '%chat%'".  !!! доработать

Все выборки складываем в один каталог (keysPath).

III. Обработка (выполняется последовательно для каждого кейворда из предыдущего пункта).
III.1. Объединяем кейворды из всех файлов в каталоге, удаляем дубли и сохраняем в один файл (см. скрипт ниже).
III.2. Чистим по блэк-листу (см. скрипт ниже) + по предыдущим напарсенным кейвордам.
III.3. Выбираем по адалт-листу (см. скрипт ниже).

IV. Общая обработка (после выборки и обработки всех кейвордов).
IV.1. Объединение файлов < 10 Kb (330 слов) в один файл "joined.txt".
IV.2. Расстановка весов для файлов.

'''

def GetWordForms(keys, mainKey):
    '''Находим словоформы кейворда'''
    keys2 = {}
    for item in keys:
        for item2 in item.split(' '):
            if item2.find(mainKey) >= 0:
                if item2 not in keys2:
                    keys2[item2] = 0
                keys2[item2] += 1
    sorted_keys2 = sorted(keys2.iteritems(), key=operator.itemgetter(1))
    print(sorted_keys2)
    for item in sorted_keys2:
        print(item)
    print('---')
    print(len(keys2))

def SimplifyWordsList(words):
    '''Сокращение списка кейвордов за счет вхождений.
    Также выводится список кейвордов, оканчивающихся на "s".'''
    wordsList = words.split('\n')
    wordsList = [item.strip().lower() for item in wordsList]
    wordsListLengthOld = len(wordsList)
    wordsListNew = []
    for item in wordsList:
        found = False
        if item.endswith('s'):
            print('s: %s' % item)
        for item2 in wordsList:
            if (item.find(item2) >= 0) and (item != item2) and (item != '') and (item2 != ''):
                found = True
                print('%s - %s' % (item, item2))
                break
        if not found:
            wordsListNew.append(item)
    wordsList = sorted(list(set(wordsListNew)))
    print('\n'.join(wordsList))
    print('---')
    print('List length: %d => %d.' % (wordsListLengthOld, len(wordsList)))
