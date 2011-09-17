# coding=utf8
import urllib, HTMLParser, operator, math

class Stripper(HTMLParser.HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
        self.recording = False
    def handle_starttag(self, tag, attributes):
        if tag == 'body':
            self.recording = True
    def handle_data(self, d):
        if self.recording:
            self.fed.append(d)
    def get_data(self):
        return ' '.join(self.fed)

blackListWords = '''
,a,an,the,
this,these,that,those,some,any,
what,which,who,whom,whose,how,
i,me,myself,mine,my,
we,us,ourselves,ourself,ours,our,
you,yourself,yourselves,yours,your,
he,him,himself,hisself,his,
she,her,herself,hers,her,
it,itself,its,
they,them,themself,themselves,theirs,their,
am,is,are,being,was,were,been,have,has,having,had,do,does,doing,did,done,
shall,will,must,can,may,
here,there,only,such,few,much,many,lot,more,all,none,no,even,already,yet,also,
and,or,not,
aboard,about,above,across,after,against,along,alongside,among,amongst,around,
as,aside,at,before,behind,below,beneath,beside,besides,between,beyond,but,by,
despite,down,during,except,excluding,following,for,from,given,in,including,
inside,into,like,near,next,of,off,on,onto,out,outside,over,past,per,plus,
regarding,round,sans,since,than,through,thru,till,to,toward,towards,under,
underneath,unlike,until,up,upon,versus,via,with,within,without
'''
blackListWords = blackListWords.replace('\n', '').split(',')
whiteListChars = 'abcdefghijklmnopqrstuvwxyz0123456789\''

def Analyze(url, showDetails = True):
    '''Получаем страницу'''
    stripper = Stripper()
    fd = urllib.urlopen(url)
    stripper.feed(fd.read())
    fd.close()
    contents = stripper.get_data()
    
    '''Анализируем'''
    items1 = {}
    total1 = 0
    total2 = 0
    for item in contents.split(' '):
        item = item.strip().lower()
        item = ''.join([c for c in item if c in whiteListChars])
        if item in blackListWords:
            continue
        if item not in items1:
            items1[item] = 0
            total2 += 1
        items1[item] += 1
        total1 += 1
    items2 = sorted(items1.iteritems(), key=operator.itemgetter(1))
    items2.reverse()
    
    '''Определяем ключевые показатели'''
    topCount = items2[0][1]
    topPercent1 = float(topCount) / total1 * 100
    topPercent2 = float(topCount) / total2 * 100
    nausea = math.sqrt(max(7, topCount))
    isGood = (topPercent1 < 8) and (topPercent2 < 30) and (nausea < 8)
    
    '''Выводим результат анализа'''
    details = ''
    details += 'url: %s\n' % url
    details += 'nausea: %.2f, %.2f%%, %.2f%%\n' % (nausea, topPercent1, topPercent2)
    details += 'good: %s\n' % isGood
    details += '---\n'
    if showDetails:
        for item in items2[:20]:
            details += '%s %.2f%%, %.2f%% (%d)\n' % (item[0].ljust(15), float(item[1]) / total1 * 100, float(item[1]) / total2 * 100, item[1])
        details += '---\n'
        details += 'total words: %d\n' % total1
        details += 'distinct words: %d\n' % total2
        details += '---\n'
    
    '''Возвращаем ключевые показатели'''
    return isGood, details

if __name__ == '__main__':
    _, details = Analyze('http://saintlouiscity.info/')
    print(details)
