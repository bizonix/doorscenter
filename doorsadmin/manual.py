# coding=utf8
from doorsadmin.models import Niche, Domain, Doorway, Host, IPAddress, GenerateSpamTasks
import re, random, urlparse

def AddDomains():
    '''Добавление доменов из файла'''
    host = Host.objects.get(pk=8)
    ipAddress = IPAddress.objects.get(pk=random.randint(14, 18))
    domainsFileName = r'./domains.txt'
    for domainName in open(domainsFileName).readlines():
        domainName = domainName.strip()
        if domainName != '':
            print(domainName)
            domainGroup = domainName.split('.')[1]
            Domain.objects.create(name=domainName, group=domainGroup, host=host, ipAddress=ipAddress).save()

rxHtml = re.compile(r'<a href="(.*)">(.*)</a>')
def ExtractUrl(link):
    '''Из ссылки получаем урл'''
    x = rxHtml.match(link)
    if not x:
        return ''
    if len(x.groups()) != 2:
        return ''
    return x.groups()[0]

def AddLinks():
    '''Добавление дорвеев и ссылок из файла (для классики)'''
    linksFileName = r'./links.txt'
    '''Читаем ссылки и группируем по хостам'''
    linksDict = {}
    for link in open(linksFileName):
        url = ExtractUrl(link)
        host = urlparse.urlparse(url).netloc
        if host not in linksDict:
            linksDict[host] = []
        linksDict[host].append(link)
    '''Создаем дорвеи и ссылки для спама'''
    niche = Niche.objects.get(pk=5)
    for host in linksDict.iterkeys():
        print(host)
        try:
            linksCount = len(linksDict[host])
            domain = Domain.objects.get(name=host.replace('www.', ''))
            domain.niche = niche
            domain.group = 'classic'
            domain.maxDoorsCount = 1
            domain.save()
            if Doorway.objects.filter(domain=domain, domainFolder=r'/').count() == 0:
                doorway = Doorway.objects.create(niche=niche, domain=domain, domainFolder=r'/', pagesCount=-1, doorLinksCount=linksCount, spamLinksCount=linksCount)
                doorway.SetTaskDetails({'doorLinksList': linksDict[host], 'state': 'done', 'lastError': '', 'runTime': None})
                doorway.stateManaged = 'done'
                doorway.save()
            else:
                raise Exception('Doorway already exists.')
        except Exception as error:
            print('Error: %s' % error)

def GenSpam():
    '''Генерируем задания для спама'''
    GenerateSpamTasks()
    
def Helper():
    '''Прочие действия из командной строки'''
    pass
