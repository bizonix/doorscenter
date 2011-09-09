# coding=utf8
import urllib, re, time

def ParseNames1(url, key, fileName):
    if key != '':
        print('parsing key %s:' % key)
    else:
        print('parsing url %s:' % url)
    names = set()
    for n in range(100):
        print('- step %d ...' % (n + 1))
        if key != '':
            fd = urllib.urlopen('http://www.tryname.ru/', urllib.urlencode({'name': key, 'act': 'send'}))
        else:
            fd = urllib.urlopen('http://www.tryname.ru/lists/' + url)
        names.update(re.findall(r"target='_blank'\>([a-z]*\.ru)\</a", fd.read()))
        fd.close()
        time.sleep(1)
    with open('/home/sasch/temp/names/' + fileName, 'a') as fd:
        fd.write('\n'.join(list(names)))
    print('- %d names total' % len(names))

def ParseNames():
    ParseNames1('eng_popular', '', 'en-common.txt')
    ParseNames1('ger_words_small', '', 'de-common.txt')
    ParseNames1('fra_words_small', '', 'fr-common.txt')
    ParseNames1('ita_popular', '', 'it-common.txt')
    ParseNames1('lat_popular', '', 'latin-common.txt')
    ParseNames1('eng_names', '', 'en-names.txt')
    ParseNames1('eng_us_counties', '', 'en-countries.txt')
    ParseNames1('eng_scientific_words', '', 'en-science.txt')
    ParseNames1('', 'xxx', 'key-xxx.txt')
    print('done')

ParseNames()
