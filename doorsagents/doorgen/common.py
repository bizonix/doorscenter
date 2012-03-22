# coding=utf8

def FindMacros(source, macrosName = ''):
    '''Находим очередной макрос. Note: находит также переменные PHP, обрамленные 
    фигурными скобками'''
    if source.find('{' + macrosName) >= 0:
        before, _, x = source.partition('{' + macrosName)
        macrosArgsList = []
        '''Идем по скобкам'''
        macrosNamePosBegin = 0
        macrosNamePosEnd = -1
        macrosArgsPosBegin = -1
        macrosArgsPosLast = -1
        macrosArgsPosEnd = -1
        macrosEnd = -1
        level1 = 1  # {}
        level2 = 0  # ()
        for n in range(len(x)):
            if x[n] == '{':
                level1 += 1
            elif x[n] == '}':
                level1 -= 1
                if (level2 == 0) and (macrosNamePosEnd == -1):  # здесь может быть конец имени макроса
                    macrosNamePosEnd = n
            elif x[n] == '(':
                if (level2 == 0) and (macrosNamePosEnd == -1):  # здесь может быть конец имени макроса
                    macrosNamePosEnd = n
                if (level2 == 0) and (macrosArgsPosBegin == -1):  # ... и начало списка аргументов
                    macrosArgsPosBegin = n
                    macrosArgsPosLast = n
                level2 += 1
            elif x[n] == ')':
                level2 -= 1
                if (level2 == 0) and (macrosArgsPosBegin != -1) and (macrosArgsPosEnd == -1):
                    macrosArgsList.append(x[macrosArgsPosLast + 1:n])
                    macrosArgsPosEnd = n
            elif x[n] == ',':
                if (level2 == 1) and (macrosArgsPosBegin != -1) and (macrosArgsPosEnd == -1):
                    macrosArgsList.append(x[macrosArgsPosLast + 1:n])
                    macrosArgsPosLast = n
            if (level1 == 0) and (level2 == 0):
                macrosEnd = n
                break
        macrosFull = '{' + macrosName + x[:macrosEnd + 1]
        macrosName = (macrosName + x[macrosNamePosBegin:macrosNamePosEnd]).upper()
        after = x[macrosEnd + 1:]
        return before, macrosFull, macrosName, macrosArgsList, after
    else:
        return '', '', '', [], source

def ReplaceNth(subject, strToFind, strToReplace, n):
    '''Заменяем nth вхождение подстроки'''
    if n <= 0:
        return subject
    pos = -1
    for _ in range(n):
        pos = subject.find(strToFind, pos + 1)
        if pos < 0:
            return subject
    return subject[:pos] + strToReplace + subject[pos + len(strToFind):]
