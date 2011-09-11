# coding=utf8
import random, glob, re

def GenPattern(minChars, maxChars):
    '''Генерируем паттерн - порядок гласных и согласных'''
    pattern = ''
    length = random.randint(minChars, maxChars)
    while len(pattern) < length:
        if random.randint(0, 1) == 0:
            pattern += 'g'
        else:
            pattern += 's'
        pattern = pattern.replace('ggg', 'gg')
        pattern = pattern.replace('ssss', 'sss')
    return pattern

def GenNamePattern(pattern):
    '''Генерируем имя по паттерну'''
    charSetG = 'aeiou'  # 'y'
    charSetS = 'bcdfghklmnprstv'  # 'jqwxz'
    
    name = ''
    charNew = ''
    charPast = ''
    for charPattern in pattern:
        if charPattern == 'g':
            charSet = charSetG
        else:
            charSet = charSetS
        while charNew == charPast:
            charNew = charSet[random.randint(0, len(charSet) - 1)]
        name += charNew
        charPast = charNew
    return name

orkGrammar = {
    "name": ["<nameStart><nameMiddle0to3><nameEnd>"],
    "nameMiddle0to3": ["","<nameMiddle>", "<nameMiddle><nameMiddle>", "<nameMiddle><nameMiddle><nameMiddle>"],
    "nameStart": ["<nsCons><nmVowel>", "<nsCons><nmVowel>", "<nsCons><nmVowel>", "<nsVowel>"],
    "nameMiddle": ["<nmCons><nmVowel>"],
    "nameEnd": ["<neCons><neVowel>", "<neCons>", "<neCons>"],
    "nsCons": ["D", "G", "K", "T", "Gr"],
    "nmCons": ["d", "g", "k", "t", "r", "s", "z", "kt", "rs", "gr"],
    "neCons": ["r", "s", "z"],
    "nsVowel": ["E", "U"],
    "nmVowel": ["a", "e", "i", "o", "u"],
    "neVowel": ["a", "u"]
}

fooGrammar = {
    "name": ["<nameStart><nameMiddle0to2><nameEnd>"],
    "nameMiddle0to2": ["","<nameMiddle>", "<nameMiddle><nameMiddle>"],
    "nameStart": ["<nsCons><nmVowel>", "<nsCons><nmVowel>", "<nsCons><nmVowel>", "<nsVowel>"],
    "nameMiddle": ["<nmCons><nmVowel>"],
    "nameEnd": ["<neCons><neVowel>", "<neCons>", "<neCons>"],
    "nsCons": ["J", "M", "P", "N", "Y", "D", "F"],
    "nmCons": ["l", "m", "lm", "th", "r", "s", "ss", "p", "f", "mb", "b", "lb", "d", "lf"],
    "neCons": ["r", "n", "m", "s", "y", "l", "th", "b", "lb", "f", "lf"],
    "nsVowel": ["A", "Au", "Ei"],
    "nmVowel": ["a", "e", "i", "o", "u", "au", "oa", "ei"],
    "neVowel": ["e", "i", "a", "au"]
}

def GenNameGrammar(minChars, maxChars):
    '''Генерируем имя по грамматике'''
    nameStr = ''
    nameGrammar = random.choice([fooGrammar, orkGrammar])
    reNonTerminal = re.compile(r"<(\w+)>")
    while (len(nameStr) < minChars) or (len(nameStr) > maxChars):
        nameStr = random.choice(nameGrammar["name"])
        matchNonTerminal = reNonTerminal.search(nameStr)
        while matchNonTerminal:
            subStr = random.choice(nameGrammar[matchNonTerminal.group(1)])
            nameStr = reNonTerminal.sub(subStr, nameStr, 1)
            matchNonTerminal = reNonTerminal.search(nameStr)
    return nameStr.lower()

def GenDomainNamesPattern(zone, count):
    '''Генерируем заданное число доменов в заданной зоне'''
    namesGenerated = []
    for _ in range(count):
        namesGenerated.append(GenNamePattern(GenPattern(6, 10)) + zone)
    return namesGenerated

def GenDomainNamesGrammar(zone, count):
    '''Генерируем заданное число доменов в заданной зоне'''
    namesGenerated = []
    for _ in range(count):
        namesGenerated.append(GenNameGrammar(6, 10) + zone)
    return namesGenerated

def GenDomainNamesTry(zone, count):
    '''Выбираем имена из списков tryname'''
    lines = []
    for fileName in glob.glob('/home/sasch/temp/names/*.txt'):
        for line in open(fileName, 'r'):
            if (len(line.strip()) >= 6) and (len(line.strip()) <= 10): 
                lines.append(line.strip())
    random.shuffle(lines)
    domainNames = [line + zone for line in lines[:count]]
    return domainNames

def GenDomainNamesSape(zone, count):
    '''Выбираем имена из списков tryname для sape по Хопкинсу'''
    lines = []
    for fileName in glob.glob('/home/sasch/temp/names/*.txt'):
        for line in open(fileName, 'r'):
            lines.append(line.strip())
    random.shuffle(lines)
    domainNames = ['%s%d%s' % (line, random.randint(10, 99), zone) for line in lines[:count]]
    return domainNames

names = GenDomainNamesPattern('.info', 20)
print('*** pattern ***')
print('\n'.join(names))
print('')

names = GenDomainNamesGrammar('.info', 20)
print('*** grammar ***')
print('\n'.join(names))
print('')

names = GenDomainNamesTry('.info', 20)
print('*** try ***')
print('\n'.join(names))
print('')

names = GenDomainNamesSape('.ru', 20)
print('*** sape ***')
print('\n'.join(names))
print('')
