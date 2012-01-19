# coding=utf8
import random, re, os, cookielib, urllib, urllib2, tempfile, datetime, HTMLParser, string

class Snippets(object):
    '''Парсер сниппетов'''
    
    def __init__(self):
        '''Инициализация'''
        self.snippetsList = []
        self.pause = 5  # время между запросами в секундах
        self.validChars = r'-%s%s.,:;!?/()[]\'" ' % (string.ascii_letters, string.digits)
        self.rxSnippet = re.compile(r'<div class=\"s\">(.+?)<br>', re.S)
        self.rxStripTags = re.compile(r'<[^>]*?>')
        self.rxStripDates = re.compile(r'[0-9]?[0-9] ... 20[0-1][0-9] ')
        self.rxStripSpaces = re.compile(r'\s+')
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
    
    def _Decapitalize(self, word):
        '''Убираем лишнюю капитализацию'''
        if word == word.upper():
            word = word.capitalize()
        return word
        
    def Parse(self, keywordsList, language):
        '''Парсинг'''
        dateTimeStart = datetime.datetime.now()
        self.snippetsList = []
        parser = HTMLParser.HTMLParser()
        for keyword in keywordsList:
            keyword = keyword.strip()
            print('- %s' % keyword)
            '''Делаем запрос'''
            url = 'http://www.google.com/search?as_q=%s&tbs=qdr:z&num=100&hl=%s&output=ie&filter=0' % (urllib.quote_plus(keyword), language)
            request = urllib2.Request(url)
            request.add_header('User-Agent', random.choice(self.userAgentsList))
            self.cookieJar.add_cookie_header(request)
            response = urllib2.urlopen(request)
            newSnippetsList = self.rxSnippet.findall(response.read())
            response.close()
            '''Обрабатываем результаты'''
            for snippet in newSnippetsList:
                snippet = parser.unescape(snippet)
                snippet = self.rxStripTags.sub('', snippet)
                snippet = self.rxStripDates.sub('', snippet)
                snippet = self.rxStripSpaces.sub(' ', snippet)
                snippet = ''.join([char for char in snippet if char in self.validChars])
                snippet = ' '.join([self._Decapitalize(word) for word in snippet.split(' ')])
                snippet = snippet.replace('...', '')
                snippet = snippet.strip()
                if len(snippet) > 60:
                    self.snippetsList.append(snippet)
        '''Отчет о проделанной работе'''
        print('Parsed %d snippets in %d sec.' % (len(self.snippetsList), (datetime.datetime.now() - dateTimeStart).seconds))
        return self.snippetsList

if __name__ == '__main__':
    snippets = Snippets()
    snippetsList = snippets.Parse(['foreign affair'], 'en')
    print('\n'.join(snippetsList))
