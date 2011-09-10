# coding=utf8
import random, glob, godaddy

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

def GenName(pattern):
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

def GenDomainNamesGD(zone, count):
    '''Генерируем заданное число доменов в заданной зоне с проверкой занятости на GD'''
    namesGenerated = []
    for _ in range(count):
        namesGenerated.append(GenName(GenPattern(6, 10)) + zone)
    gdApi = godaddy.GoDaddyAPIReal()
    namesAvailableDict = gdApi.CheckAvailability(namesGenerated)
    namesAvailableList = [name for name in namesAvailableDict if namesAvailableDict[name]]
    return namesAvailableList

def GenDomainNamesSape(zone, count):
    '''Генерируем имена из списка tryname для sape'''
    lines = []
    for fileName in glob.glob('/home/sasch/temp/names/*.txt'):
        for line in open(fileName, 'r'):
            lines.append(line.strip())
    random.shuffle(lines)
    domainNames = ['%s%d%s' % (line, random.randint(10, 99), zone) for line in lines[:count]]
    return domainNames

names = GenDomainNamesSape('.ru', 20)
print('%d names:' % len(names))
print('\n'.join(names))
