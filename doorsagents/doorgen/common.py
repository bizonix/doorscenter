# coding=utf8

def FindMacros(source, macrosName = ''):
    '''Находим очередной макрос'''
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


'''
print(FindMacros('123456'))
print(FindMacros('123{}456'))
print(FindMacros('123{NAME}456'))
print(FindMacros('{NAME}456'))
print(FindMacros('123{NAME}'))
print(FindMacros('123{NAME()}456'))
print(FindMacros('123{NAME()()}456'))
print(FindMacros('123{NAME(1)}456'))
print(FindMacros('123{NAME(1,2)}456'))
print(FindMacros('123{NAME(11,22,33)}456'))
print(FindMacros('123{NAME(1,,,4)}456'))
print(FindMacros('123{NaMe}456'))
print(FindMacros('123{NAME({FOR(1,2)},{FOR(3,4)})}456'))

sys.exit()
'''
