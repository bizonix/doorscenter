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

names = GenDomainNamesPast('.info', 20)
print('*** past common (%d) ***' % len(names))
print('\n'.join(names))
print('')

names = GenDomainNamesPast('.info', 20, 'dat')
print('*** past dat (%d) ***' % len(names))
print('\n'.join(names))
print('')
