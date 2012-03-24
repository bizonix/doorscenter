# coding=utf8
import os, sys, operator, kwk8
from keysupdaterlib import adultWords, blackWords

''' Автоматический парсинг кейвордов

  Этапы парсинга:

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

'''Находим словоформы кейворда'''
'''
mainKeyword = 'chat'
keys2 = {}
for item in keys:
    for item2 in item.split(' '):
        if item2.find(mainKeyword) >= 0:
            if item2 not in keys2:
                keys2[item2] = 0
            keys2[item2] += 1
sorted_keys2 = sorted(keys2.iteritems(), key=operator.itemgetter(1))
print(sorted_keys2)
for item in sorted_keys2:
    print(item)
#keys2 = sorted(list(set(keys2)))
#print('\n'.join(keys2))
print('---')
print(len(keys2))
sys.exit(0)'''

'''Объединяем кейворды из всех файлов в каталоге, удаляем дубли и сохраняем в один файл'''
keysPath = r'c:\Work\keys2\chat1'
keys = []
for fileName in os.listdir(keysPath):
    for item in open(os.path.join(keysPath, fileName)):
        keys.append(item.strip().replace('"', '').replace('+', ''))
keys = list(set(keys))
with open(os.path.join(keysPath, '..', 'chat-all.txt'), 'w') as fd:
    fd.write('\n'.join(keys))
print(len(keys))

'''Чистим по блэк-листу'''
kwk8.Kwk8Keys(os.path.join(r'c:\Work\keys2', 'chat-all.txt'), True).DeleteByList(blackWords.split('\n')).Save(os.path.join(r'c:\Work\keys2', 'chat-clear.txt'))

'''Выбираем по адалт-листу'''
kwk8.Kwk8Keys(os.path.join(r'c:\Work\keys2', 'chat-clear.txt'), True).SelectByList(adultWords.split('\n')).Save(os.path.join(r'c:\Work\keys2', 'chat-adult.txt'))

