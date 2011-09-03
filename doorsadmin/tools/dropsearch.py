# coding=utf8
import urllib, urllib2, json, sys, godaddy, time, datetime

opener = urllib2.build_opener()
opener.addheaders.append(('Host', 'seodor.ru'))
opener.addheaders.append(('User-Agent', 'Mozilla/5.0 (X11; Linux i686; rv:6.0.1) Gecko/20100101 Firefox/6.0.1'))
opener.addheaders.append(('Accept', '*/*'))
opener.addheaders.append(('Accept-Language', 'ru,en-us;q=0.7,en;q=0.3'))
opener.addheaders.append(('Accept-Encoding', 'gzip, deflate'))
opener.addheaders.append(('Accept-Charset', 'windows-1251,utf-8;q=0.7,*;q=0.7'))
opener.addheaders.append(('Connection', 'keep-alive'))
opener.addheaders.append(('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'))
opener.addheaders.append(('X-Requested-With', 'XMLHttpRequest'))
opener.addheaders.append(('Referer', 'http://seodor.ru/drop/search.php'))
opener.addheaders.append(('Cookie', 'ids=392716%2C360667%2C412156%2C398503%2C378384%2C357007%2C376179%2C362302%2C360648%2C419673%2C357441%2C399019%2C363392%2C377660%2C403300%2C410614%2C376254%2C392812; id=22; hash=66996dffadc71dda1f6865c314ae3fe4'))
opener.addheaders.append(('Pragma', 'no-cache'))
opener.addheaders.append(('Cache-Control', 'no-cache'))

data = {'ids': '', 'min_year': '1996', 'max_year': '2008', 'min_record': '0', 'max_record': '999999', 'min_pr': '0', 'max_pr': '10', 'min_tic': '0', 'max_tic': '9999999', 'min_backlinks': '0', 'max_backlinks': '1000', 'min_alexa_rank': '0', 'max_alexa_rank': '999999999', 'min_google_index': '10', 'max_google_index': '999999999', 'min_yahoo_index': '0', 'max_yahoo_index': '999999999', 'min_yandex_index': '0', 'max_yandex_index': '999999999', 'min_time_expire': '01-01-1970', 'max_time_expire': '04-09-2011', 'sort': 'google_index', 'sort_type': 'desc', 'page': '1'}
data['max_time_expire'] = datetime.date.today().strftime('%d-%m-%Y')
data['com_zone'] = 'on'

'''Parsing the seodor/drop'''
domainsParsed = []
for page in range(1,6):  # to +1
    print('Parsing page %d ...' % page)
    data['page'] = page
    fd = opener.open('http://seodor.ru/drop/search_ajax.php', urllib.urlencode(data))
    for item in json.loads(fd.read()):
        if type(item) == type({}):
            domainsParsed.append(item['domain'])
    fd.close()
    time.sleep(2)
print('%d domains parsed.' % len(domainsParsed))

'''Checking domains availability'''
gdApi = godaddy.GoDaddyAPIReal()
availability = gdApi.CheckAvailability(domainsParsed)
domainsAvailable = []
for item in availability:
    if availability[item]:
        domainsAvailable.append(item)
print('%d domains available:' % len(domainsAvailable))
print('\n'.join(domainsAvailable))
