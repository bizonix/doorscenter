# coding=utf8
import urlparse, operator, threading, Queue, re, time, datetime, googleproxy

googleResultsStrList = [r'About ([0-9,]*) res', r'of about <b>([0-9,]*)</b>', r'<div>([0-9,]*) res']
googleNoResultsStr1 = 'No results found for'
googleNoResultsStr2 = 'did not match any documents'

monitorCancelled = True

def FindFreeHosts(baseFileName, minHosts=500):
    '''Находим популярные фрихосты'''
    global monitorCancelled

    '''Получаем словарь "хост второго уровня": "число сайтов"'''
    n = 0
    hostsDict = {}
    for url in open(baseFileName):
        try:
            host = urlparse.urlparse(url).netloc
            hostPartsList = host.split('.')
            if len(hostPartsList) <= 2:
                continue
            hostTopName = hostPartsList[-2] + '.' + hostPartsList[-1]
            if hostTopName not in hostsDict:
                hostsDict[hostTopName] = 0
            hostsDict[hostTopName] += 1
        except Exception as error:
            print(error)
        n += 1
        if n % 100000 == 0:
            print('- %d ...' % n)
    
    '''В словаре находим хосты с числом сайтов больше 10'''
    hostsDict = dict((key, value) for key, value in hostsDict.iteritems() if value >= minHosts)
    hostsList = sorted(hostsDict.iteritems(), key=operator.itemgetter(1), reverse=True)
    queryString = 'https://www.google.com/search?q=site:.%s&hl=en&safe=off&tbs=qdr:d'
    queriesList = [queryString % item[0] for item in hostsList]
    infoList = ['%s: %d' % (item[0], item[1]) for item in hostsList]
    
    '''Выводим результаты'''
    print('Results: %d' % len(hostsList))
    print('\n'.join(queriesList))
    print('\n'.join(infoList))
    #hostsList = [('wordpress.com', 99275),('co.uk', 84730),('webs.com', 31196),('com.au', 26816),('co.kr', 19616),('livejournal.com', 19571),('ning.com', 19414),('fc2.com', 18762),('typepad.com', 16024),('deviantart.com', 14456),('org.uk', 13011),('com.br', 12877),('wetpaint.com', 12268),('com.ua', 11851),('free.fr', 11245),('forumer.com', 11022),('co.za', 9697),('hi5.com', 9074),('at.ua', 9054),('forumotion.com', 8861),('splinder.com', 8605),('hubpages.com', 8012),('forumcommunity.net', 7585),('co.cc', 7448),('narod.ru', 7436),('yuku.com', 7164),('com.ph', 6989),('altervista.org', 6419),('tripod.com', 6312),('com.cn', 6187),('forumfree.it', 6135),('com.ar', 5983),('dig10.in', 5817),('co.nz', 5789),('mylivepage.com', 5726),('forumotion.net', 5542),('blogdrive.com', 5520),('free-press-release.com', 5237),('blogbugs.org', 5153),('ne.jp', 5126),('cocolog-nifty.com', 5064),('promodj.com', 5041),('bloog.pl', 4975),('no-ip.org', 4755),('org.ua', 4681),('friendpages.com', 4583),('ucoz.com', 4579),('moikrug.ru', 4477),('forumactif.com', 4356),('istmein.de', 4347),('blog.com', 4334),('guildlaunch.com', 4311),('pdj.com', 4309),('blog.ru', 4199),('kurman.ru', 4169),('wikia.com', 4009),('funpic.de', 3990),('xanga.com', 3912),('ez-dns.com', 3808),('fotopages.com', 3731),('land.ru', 3601),('co.jp', 3590),('net.ru', 3564),('org.au', 3537),('tumblr.com', 3519),('com.tw', 3465),('mygb.nl', 3367),('netfirms.com', 3305),('style.it', 3185),('or.kr', 3156),('onsugar.com', 3111),('forumactif.net', 3098),('piczo.com', 3021),('dumbmachine.net', 2942),('multiply.com', 2906),('mojeforum.net', 2862),('do.am', 2846),('blog.hr', 2817),('meetup.com', 2805),('dreamwidth.org', 2693),('e-monsite.com', 2693),('angelfire.com', 2665),('posterous.com', 2636),('hotbox.ru', 2554),('web-log.nl', 2515),('sapo.pt', 2457),('wrzuta.pl', 2435),('filedudes.com', 2419),('skynetblogs.be', 2402),('tribe.net', 2367),('co.il', 2286),('pixnet.net', 2244),('ucoz.ua', 2236),('page.tl', 2235),('ac.uk', 2210),('humanarchives.org', 2193),('softonic.com', 2144),('yoyo.pl', 2142),('bytechase.cx', 2141),('net.ua', 2115),('promodj.ru', 2096),('kiev.ua', 2083),('metadns.cx', 2077),('forum24.ru', 2059),('forumeiros.com', 2040),('dyns.net', 2032),('doomdns.com', 2028),('foren-city.de', 2019),('ec21.com', 2014),('bee.pl', 1977),('rusmarket.ru', 1974),('com.pl', 1973),('weddingannouncer.com', 1923),('ucoz.net', 1916),('mysbrforum.com', 1902),('ac.th', 1882),('suddenlaunch.com', 1872),('cba.pl', 1865),('rusmarket.com', 1853),('informe.com', 1842),('hostlogr.com', 1812),('narod2.ru', 1801),('nm.ru', 1796),('darkbb.com', 1783),('webovastranka.cz', 1779),('weekend.lu', 1778),('edu.tw', 1767),('org.ru', 1762),('suite101.com', 1761),('edublogs.org', 1725),('co.in', 1717),('exblog.jp', 1715),('tistory.com', 1686),('canalblog.com', 1651),('no12u.bz', 1640),('go.th', 1634),('centerblog.net', 1633),('forumprofi.de', 1624),('spb.ru', 1621),('com.my', 1619),('myfreeforum.org', 1616),('informer.com', 1614),('gov.cn', 1597),('pdj.ru', 1594),('net.au', 1590),('freeservers.com', 1590),('nabble.com', 1585),('front.ru', 1585),('cafe24.com', 1582),('egloos.com', 1575),('forumpro.fr', 1573),('ob.tc', 1560),('forum2x2.ru', 1559),('bloger.hr', 1555),('blogfree.net', 1554),('dyns.be', 1549),('yoo7.com', 1548),('net.cn', 1547),('ac.kr', 1543),('downloadsoftware4free.com', 1517),('blogs.com', 1517),('blog.cz', 1511),('8m.com', 1510),('ac.id', 1506),('edu.au', 1502),('dyndns.org', 1489),('uw.hu', 1488),('bravehost.com', 1478),('fr.nf', 1476),('forum24.se', 1447),('strefa.pl', 1428),('fromru.su', 1391),('com.mx', 1391),('electrob.ru', 1391),('forumieren.com', 1377),('jcink.com', 1363),('gdf-jorge-antunes.com', 1360),('forumco.com', 1345),('mytinybaby.com', 1343),('eforum.lt', 1332),('forumieren.de', 1304),('pledgepage.org', 1298),('t35.me', 1285),('cams1.ws', 1283),('4t.com', 1280),('pornblink.com', 1259),('pornlivenews.com', 1258),('bonafidelive.com', 1255),('waqn.com', 1253),('i.ph', 1249),('forummotion.com', 1246),('activeboard.com', 1235),('websitetoolbox.com', 1227),('com.vn', 1219),('awardspace.com', 1216),('sosblogs.com', 1201),('myfri3nd.com', 1189),('myforum.ro', 1173),('blogonline.ru', 1172),('in.ua', 1171),('monforum.com', 1165),('tribenetwork.com', 1165),('bravejournal.com', 1163),('textcube.com', 1162),('zip2save.com', 1157),('0pk.ru', 1148),('org.nz', 1147),('kilu.de', 1146),('adultsearch.com', 1141),('uservoice.com', 1135),('pissedconsumer.com', 1133),('friendster.com', 1130),('top-site-list.com', 1124),('omgforum.net', 1121),('co.nr', 1119),('mybb.ru', 1107),('pbworks.com', 1105),('edu.cn', 1102),('cp.cx', 1101),('in.th', 1088),('wikidot.com', 1085),('uhumba.com', 1084),('showmember.com', 1078),('110mb.com', 1069),('smf4u.com', 1061),('8k.com', 1055),('gqitalia.it', 1053),('stroyportal.su', 1047),('com.sg', 1045),('superforum.fr', 1044),('001webs.com', 1039),('iblog2011.com', 1030),('cscblog.jp', 1029),('over-blog.com', 1028),('magix.net', 1028),('ucoz.kz', 1024),('businesscard2.com', 1019),('dyndns-web.com', 1014),('sxsy.co', 1008),('alltop.com', 1005),('weebly.com', 1002)]
    
    '''Помещаем группу в очередь'''
    dateTimeStart = datetime.datetime.now()
    queueIn = Queue.Queue()
    queueOut = Queue.Queue()
    for item in hostsList:
        queueIn.put(item[0])
    
    '''Загружаем прокси'''
    proxyList = googleproxy.GoogleProxiesList()
    #proxyList.Update()

    '''Проверка'''
    threadsCount = 100
    monitorCancelled = False
    KeywordsCheckerMonitor(queueIn, queueOut, proxyList, len(hostsList)).start()
    for _ in range(threadsCount):
        KeywordsChecker(queueIn, queueOut, proxyList).start()
    queueIn.join()
    monitorCancelled = True
    
    '''Статистика'''
    timeDelta = (datetime.datetime.now() - dateTimeStart).seconds
    print('Checked %d keywords in %d sec. (%.2f sec./keyword)' % (len(hostsList), timeDelta, timeDelta * 1.0 / len(hostsList)))

    
class KeywordsChecker(threading.Thread):
    '''Поточный чекер кейвордов в гугле'''

    def __init__(self, queueIn, queueOut, proxyList):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True
        self.queueIn = queueIn
        self.queueOut = queueOut
        self.proxyList = proxyList
        self.rxList = [re.compile(item) for item in googleResultsStrList]

    def run(self):
        '''Обработка очередей'''
        while not self.queueIn.empty():
            host = self.queueIn.get()
            data = self.GetData(host)
            print('- %s: %d' % (host, data))
            self.queueOut.put({host: data})
            self.queueIn.task_done()
    
    def GetData(self, host):
        '''Делаем запрос в гугл'''
        attemptsCount = 200
        for _ in range(attemptsCount):
            proxy = self.proxyList.GetRandom()
            if not proxy.googleAccess:
                continue
            #print('-- %s: %s' % (keyword, proxy))
            html = proxy.Request(host)
            if not proxy.googleAccess:
                #print('### Proxy failed: %s' % proxy)
                continue
            if html == '':
                continue
            if (html.find(googleNoResultsStr1) >= 0) or (html.find(googleNoResultsStr2) >= 0):
                return 0
            for rx in self.rxList:
                try:
                    return int(rx.findall(html)[0].replace(',', ''))
                except Exception:
                    pass
            #print(html)
        return -1

class KeywordsCheckerMonitor(threading.Thread):
    '''Монитор чекера прокси'''
    
    def __init__(self, queue1, queue2, proxyList, keywordsListCount):
        '''Инициализация'''
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue1 = queue1
        self.queue2 = queue2
        self.proxyList = proxyList
        self.keywordsListCount = keywordsListCount
        self.queue1InitialSize = self.queue1.qsize()
        
    def run(self):
        global monitorCancelled
        print('Monitoring started.')
        lastActionTime1 = time.time()
        lastActionTime2 = time.time()
        while not monitorCancelled:
            '''Каждые N секунд выводим текущую информацию'''
            if time.time() - lastActionTime1 > 5:
                offset = self.queue1InitialSize - self.queue1.qsize()
                print('... %d/%d (%.2f%%).' % (offset, self.keywordsListCount, offset * 100.0 / self.keywordsListCount))
                lastActionTime1 = time.time()
            '''Каждые X секунд апдейтим прокси'''
            if time.time() - lastActionTime2 > 60 * 3:
                self.proxyList.Update()
                lastActionTime2 = time.time()
            time.sleep(1)
        print('Monitoring finished.')

if __name__ == '__main__':
    baseFileName = r'c:\temp\LinksList id4.txt'
    FindFreeHosts(baseFileName)
