# coding=utf8
import random, godaddy

def GenPattern(minChars, maxChars):
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

def GenDomainNames(zone, count):
    namesGenerated = []
    for _ in range(count):
        namesGenerated.append(GenName(GenPattern(6, 10)) + zone)
    gdApi = godaddy.GoDaddyAPIReal()
    namesAvailableDict = gdApi.CheckAvailability(namesGenerated)
    namesAvailableList = [name for name in namesAvailableDict if namesAvailableDict[name]]
    return namesAvailableList

names = GenDomainNames('.info', 20)
print('%d names:' % len(names))
print('\n'.join(names))
