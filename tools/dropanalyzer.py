# coding=utf8

import os, re, sys, random, cookielib, tempfile, datetime, urllib2

'''
Для сайтов по списку возвращает:
- число страниц в гугле;
- число бэков в гугле, и их список;
- ссылку на одну страницу из кэша гугла.
'''

class DropAnalyzer(object):
    '''Анализ списка дропов'''
    
    def __init__(self):
        '''Инициализация'''
        self.pause = 5  # время между запросами в секундах
        self.resultsList = [r'About ([0-9,]*) res', r'of about <b>([0-9,]*)</b>', r'<div>([0-9,]*) res']
        self.rxResultsList = [re.compile(item) for item in self.resultsList]
        self.rxCache = re.compile(r'webcache[^"]*')
        self.userAgentsList = '''Opera/10.00 (Windows NT 5.1; U; ru) Presto/2.2.0
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.2; OfficeLiveConnector.1.3; OfficeLivePatch.0.0; .NET CLR 3.5.30729; .NET CLR 3.0.30618)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 1.1.4322; InfoPath.1)
Opera/9.62 (Windows NT 5.1; U; ru) Presto/2.1.1
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; GTB5; MRSPUTNIK 2, 0, 1, 31 SW; MRA 5.2 (build 02415); .NET CLR 1.1.4322; InfoPath.2; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)
Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 1.1.4322)
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FunWebProducts; (R1 1.5); .NET CLR 1.1.4322)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; FunWebProducts; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.1)
Mozilla/5.0 (Windows; U; Windows NT 5.1; pl; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1)
Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11
Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.8.0.6) Gecko/20060728 Firefox/1.5.0.6
Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)
Opera/9.25 (Windows NT 5.1; U; pl)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; AT&amp;T CSM6.0; .NET CLR 1.1.4322)
Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.7) Gecko/20060909 Firefox/1.5.0.7
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FDM)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.04506.30; InfoPath.2)
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; .NET CLR 2.0.50727)
Opera/9.20 (Windows NT 5.1; U; ru)
Opera/9.23 (Windows NT 5.1; U; ru)
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FileDownloader; .NET CLR 1.0.3705; .NET CLR 1.1.4322; InfoPath.1; FileDownloader; Media Center PC 4.0; .NET CLR 2.0.50727; MEGAUPLOAD 2.0)
Opera/9.21 (Windows NT 5.0; U; ru)
Opera/9.25 (Windows NT 5.1; U; bg)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; PeoplePal 3.0)
Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1); afcid=Wadf57d6951da76af4c6f0b08181c298d
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; MEGAUPLOAD 2.0)
Opera/8.54 (Windows NT 5.1; U; ru)
Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; YComp 5.0.0.0; .NET CLR 1.0.3705; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648)SAMSUNG-SGH-P910/1.0 SHP/VPP/R5 NetFront/3.3 SMM-MMS/1.2.0 profile/MIDP-2.0 configuration/CLDC-1.1
Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; ADVPLUGIN|K115|165|S548873517|dial; 666XXX040507; .NET CLR 2.0.50727)'''.split('\n')
        self.cookieJar = cookielib.LWPCookieJar(os.path.join(tempfile.gettempdir(), '.google-cookie'))
        try:
            self.cookieJar.load()
        except Exception:
            pass
    
    def Request(self, url):
        '''Выполняем запрос ...'''
        html = ''
        try:
            request = urllib2.Request(url)
            request.add_header('User-Agent', random.choice(self.userAgentsList))
            self.cookieJar.add_cookie_header(request)
            response = urllib2.urlopen(request)
            self.cookieJar.extract_cookies(response, request)
            html = response.read()
            response.close()
        except Exception:
            pass
        '''... из ответа получаем число результатов ...'''
        indexCount = None
        cacheLink = ''
        for rx in self.rxResultsList:
            try:
                indexCount = int(rx.findall(html)[0].replace(',', ''))
            except Exception:
                pass
        if indexCount != None:
            if indexCount > 0:
                '''... и первую страницу кэша'''
                try:
                    cacheLink = 'http://' + self.rxCache.search(html).group(0).replace('&amp;', '&')
                except Exception:
                    pass
        else:
            #print('Error getting index counting')
            pass
        return indexCount, cacheLink
    
    def Process(self, domainsList, fileName):
        '''Парсинг доменов'''
        print('Parsing domains ...')
        dateTimeStart = datetime.datetime.now()
        self.Request('http://www.google.com/')
        domainLinks = '<table>\n'
        domainsList = sorted(domainsList)
        for domain in domainsList:
            domain = domain.strip()
            urlIndex = 'http://www.google.com/search?hl=en&q=site:%s&btnG=Google+Search' % domain
            indexCount, cacheLink = self.Request(urlIndex)
            urlLinks = 'http://www.google.com/search?hl=en&q=%s+-inurl:%s&btnG=Google+Search' % (domain, domain)
            linksCount, _ = self.Request(urlLinks)
            try:
                print('- %s: %d, %d, %s' % (domain, indexCount, linksCount, 'yes' if cacheLink != '' else 'no cache'))
                if (indexCount > 0) and (cacheLink != ''):
                    domainLinks += '  <tr bgcolor="#F8F8F8">\n'
                    domainLinks += '    <td>%s</td>\n' % domain
                    domainLinks += '    <td><a href="%s" target="_blank">cache</a><td>\n' % cacheLink
                    domainLinks += '    <td><a href="%s" target="_blank">index</a> (%d)<td>\n' % (urlIndex, indexCount)
                    domainLinks += '    <td><a href="%s" target="_blank">links</a> (%d)<td>\n' % (urlLinks, linksCount)
                    domainLinks += '    <td><a href="http://whois.domaintools.com/%s" target="_blank">tools</a><td>\n' % domain
                    domainLinks += '    <td><a href="http://www.alexa.com/siteinfo/%s" target="_blank">alexa</a><td>\n' % domain
                    domainLinks += '  </tr>\n'
            except Exception:
                print('- %s: no data' % domain)
            open(fileName, 'w').write(domainLinks)  # пишем в файл после каждой итерации во избежание потери данных
        domainLinks += '</table>\n'
        open(fileName, 'w').write(domainLinks)  # пишем в файл после каждой итерации во избежание потери данных
        print('Parsed %d domains in %d sec.' % (len(domainsList), (datetime.datetime.now() - dateTimeStart).seconds))

if __name__ == '__main__':
    domainsList = ['mail.ru', 'lenta.ru']
    domainsList = ['137thsquad.com','300dateideas.com','52dollar.com','abnormalpray.com','accentsonbeauty.com','aceclef.com','agentsline.com','ahyongcheng.com','alysgifts.com','anaheim-angels-fans.com','anniekarl.com','arlanz.com','armenianrappers.com','arq-net.com','asiacub.com','automatedbusinesssolution.com','baboonblvd.com','babyhutch.com','bamabeachhouse.com','bia-uk.com','bklynbasements.com','bleedingblues.com','bodyremedyhouston.com','brandonandheather.com','byteupdate.com','cafebm.com','caraudiovideoonline.com','cardiovalencia.com','chotay.com','christjob.com','cinema-town.com','clangan.com','classroomchronicle.com','cngoldenglobe.com','commercialnuke.com','costaricarealtynow.com','criticalclothing.com','decoaccentcandle.com','desertroseint.com','dividigital.com','doctorschoicecoffee.com','doorcountywisconsinrealestate.com','drygulchmercantile.com','e-gympie.com','easylondonproperty.com','edmontonesks.com','egamepost.com','eyelists.com','fft1.com','flsteen.com','foodmanchew.com','freedom-ranch.com','furnitureoutletsuperstore.com','gdxyjd.com','ghostboarders.com','gibsonandjames.com','givinggoodness.com','glassandclaycreations.com','gpscellularphone.com','haeksan.com','hairybushgirls.com','healthclubshop.com','hengdingkj.com','hgseal.com','hiptothetrip.com','hk159.com','holloweenball.com','hrvhs1984.com','ibuyzone.com','iherbalshop.com','infinitefour.com','infodesert.com','iranbanners.com','jbrannan.com','jimsjolts.com','journalismfan.com','jt500.com','lakehurstmall.com','laserlansing.com','latin-craft.com','latinapetite.com','lavallaprototype.com','lederural.com','leenarotondo.com','lionheadrabbitclub.com','liquidvenus.com','lostinthenoise.com','madisoncountyproperty.com','merabus.com','michelleformiami.com','midwestwanderers.com','mikeandcolette.com','musee-du-chien.com','mustafabekar.com','mysearchcamel.com','nabbamexico.com','namitz.com','nastyuk.com','newlifeseminars.com','ohpinions.com','okjrquizzing.com','pageup-ffm.com','pais-colombia.com','parrillaliberty.com','peacefulskies.com','peoples-franchise.com','pinocarcelli.com','pinocchioclay.com','pmc-cis.com','powwowpawn.com','premashop.com','projectmanagementadvisory.com','ratetheattraction.com','rdbuchner.com','refinance-sandiego.com','refurbdept.com','rocketman19.com','rrtex.com','searchbao.com','sellingthemidsouth.com','senaelectronic.com','sexycumsuckers.com','shopatstore.com','sillnod.com','sinozenith.com','skylinecontractor.com','snowbump.com','songwritersq-a.com','soulfunkydisco.com','sourenco.com','stlstudios.com','sunnyforever.com','swingcontent.com','szwanyo.com','ta-planet.com','tareasweb.com','technologyoutlets.com','temposan.com','theleadexchange.com','therighthouseforme.com','thesa-key.com','tj-dc.com','tnhomesforrent.com','top9china.com','trinityhomeloans.com','trreadmill.com','v-para.com','webfifa.com','xingyenet.com','yynow.com']
    DropAnalyzer().Process(domainsList, r'c:\Temp\8\drops2.html')
