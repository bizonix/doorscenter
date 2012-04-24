# coding=utf8
from doorsadmin.models import Domain, Doorway, Host, IPAddress
import re, random, urlparse

def AddDomains():
    '''Добавление доменов из файла'''
    host = Host.objects.get(pk=8)
    ipAddress = IPAddress.objects.get(pk=random.randint(14, 18))
    domainsFileName = r'/home/admin/searchpro.name/doorscenter/domains.txt'
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
    linksFileName = r'/home/admin/searchpro.name/doorscenter/links.txt'
    linksDict = {}
    for link in open(linksFileName):
        url = ExtractUrl(link)
        host = urlparse.urlparse(url).netloc
        if host not in linksDict:
            linksDict[host] = []
        linksDict[host].append(link)
    for host in linksDict.iterkeys():
        domain = Domain.objects.get(name=host)
        linksCount = len(linksDict[host])
        if domain != None:
            domain.group = 'classic'
            domain.save()
            doorway = Doorway.objects.create(domain=domain, domainFolder=r'/', pagesCount=-1, doorLinksCount=linksCount, spamLinksCount=linksCount)
            doorway.SetTaskDetails({'doorLinksList': linksDict[host], 'state': 'done', 'lastError': '', 'runTime': None})
            doorway.stateManaged = 'done'
            doorway.save()
        else:
            print('Domain %s not found' % host)
    
def Helper():
    '''Прочие действия из командной строки'''
    pass
