# coding=utf8
import re, random, urlparse

# ключи|текст|алгоритм|категории|папка на диске|урл дора|шаблон|профиль|ftp server|ftp login|ftp pwd|ftp folder|ключей от|ключей до|плотность от|плотность до
packetTemplate = '[RANDOM]|[RANDOM]|1|none.txt|public_html/{0}/web|http://www.{0}/|hamptongaystory.co.uk|current.xml|ftp.narod.ru|login|pwd|/public_html/{0}/web|5000|7000|5|7'

domains = '''joemarkdesigns.com
cn-electronic.com
lifeskills-plus.com
willshad.com
chicagobearsfanforum.com
kerrieden.com
nlchessfest.com
ktaiwanita.com
bizoptest.com
mastinesdecuba.com'''

def GeneratePacketTask():
    '''Генерируем пакетку'''
    for domain in domains.splitlines():
        if domain.strip() != '':
            print(packetTemplate.format(domain.strip()))

linksFileName = r'C:\Work\pandora\data\logs\pack_24.04.2012_14.51.44\links.txt'

rxHtml = re.compile(r'<a href="(.*)">(.*)</a>')
def ExtractUrl(link):
    '''Из ссылки получаем урл'''
    x = rxHtml.match(link)
    if not x:
        return ''
    if len(x.groups()) != 2:
        return ''
    return x.groups()[0]

def ProcessLinks():
    '''Отбираем нужное число ссылок'''
    linksDict = {}
    '''Читаем все ссылки'''
    for link in open(linksFileName):
        url = ExtractUrl(link)
        host = urlparse.urlparse(url).netloc
        if host not in linksDict:
            linksDict[host] = []
        linksDict[host].append(link)
    '''Оставляем заданное число процентов и формируем конечный список'''
    linksList = []
    for host in linksDict.iterkeys():
        pagesCount = len(linksDict[host]) * random.randint(10, 20) / 100  # оставляем 10-20 процентов ссылок
        linksList.extend(linksDict[host][:pagesCount])
    '''Пишем его в файл'''
    open(linksFileName.replace('.txt', '-out.txt'), 'w').writelines(linksList)
    print('Done')
    
if __name__ == '__main__':
    ProcessLinks()
