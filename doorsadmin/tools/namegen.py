# coding=utf8
import random, glob, godaddy

def GenDomainNamesPast(zone, count, niche = None):
    '''Выбираем из базы Пастухова'''
    if niche:
        fileName = '/home/sasch/temp/names-past/names-%s.txt' % niche
    else:
        fileName = '/home/sasch/temp/names-past/names%.2d.txt' % random.randint(1, 72)
    with open(fileName) as fd:
        lines = fd.readlines()
    random.shuffle(lines)
    domainNames1 = [line.strip() + zone for line in lines[:count]]
    gdApi = godaddy.GoDaddyAPIReal()
    domainNames2 = gdApi.CheckAvailability(domainNames1)
    domainNames3 = [name for name in domainNames2 if domainNames2[name]]
    return domainNames3

def GenDomainNamesSape(zone, count):
    '''Выбираем имена из списков tryname для sape по Хопкинсу'''
    lines = []
    for fileName in glob.glob('/home/sasch/temp/names-try/*.txt'):
        for line in open(fileName, 'r'):
            lines.append(line.strip())
    random.shuffle(lines)
    domainNames = ['%s%d%s' % (line, random.randint(10, 99), zone) for line in lines[:count]]
    return domainNames

names = GenDomainNamesPast('.info', 30)
print('*** past common (%d) ***' % len(names))
print('\n'.join(names))
print('')

names = GenDomainNamesPast('.info', 30, 'dat')
print('*** past dat (%d) ***' % len(names))
print('\n'.join(names))
print('')

names = GenDomainNamesPast('.info', 30, 'gay')
print('*** past gay (%d) ***' % len(names))
print('\n'.join(names))
print('')

names = GenDomainNamesSape('.ru', 20)
print('*** sape (%d) ***' % len(names))
print('\n'.join(names))
print('')
