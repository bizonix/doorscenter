# coding=utf8
from __future__ import print_function
import time, hmac, hashlib, base64, urllib, sys, os, re
from BeautifulSoup import BeautifulSoup

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # убираем буферизацию stdout

class Amazon(object):
    '''Парсер Амазона'''
    
    def __init__(self):
        '''Инициализация'''
        dataList = open('amazon.ini').read().splitlines()
        self.accessKeyID = dataList[0]
        self.secretAccessKey = dataList[1]
        self.assotiateTag = dataList[2]
        self.searchIndexes = ('All','Apparel','Appliances','ArtsAndCrafts','Automotive','Baby','Beauty','Books','Classical','DigitalMusic',
            'Grocery','DVD','Electronics','HealthPersonalCare','HomeGarden','Industrial','Jewelry','KindleStore','Kitchen','LawnAndGarden',
            'Magazines','Marketplace','Merchants','Miscellaneous','MobileApps','MP3Downloads','Music','MusicalInstruments','MusicTracks',
            'OfficeProducts','OutdoorLiving','PCHardware','PetSupplies','Photo','Shoes','Software','SportingGoods','Tools','Toys','UnboxVideo',
            'VHS','Video','VideoGames','Watches','Wireless','WirelessAccessories')
        self.searchIndexesSort = {'All': [''],
            'Apparel': ['relevancerank', 'salesrank'],
            'Appliances': ['salesrank','pmrank','relevancerank','reviewrank'],
            'ArtsAndCrafts': ['pmrank','relevancerank','reviewrank'],
            'Automotive': ['salesrank'],
            'Baby': ['psrank','salesrank'],
            'Beauty': ['pmrank','salesrank'],
            'Books': ['relevancerank','salesrank','reviewrank'],
            'Classical': ['psrank','salesrank'],
            'DigitalMusic': [''],
            'DVD': ['relevancerank','salesrank'],
            'Electronics': ['pmrank','salesrank','reviewrank'],
            'Grocery': ['relevancerank','salesrank'],
            'HealthPersonalCare': ['pmrank','salesrank'],
            'HomeImprovement': ['salesrank'],
            'Industrial': ['pmrank','salesrank'],
            'Jewelry': ['pmrank','salesrank'],
            'KindleStore': ['relevancerank','reviewrank'],
            'Kitchen': ['pmrank','salesrank'],
            'LawnAndGarden': ['relevancerank','reviewrank','salesrank'],
            'Magazines': ['subslot-salesrank','reviewrank'],
            'Marketplace': ['salesrank'],
            'Merchants': ['relevancerank','salesrank'],
            'Miscellaneous': ['pmrank','salesrank'],
            'MobileApps': ['pmrank','relevancerank','reviewrank'],
            'MP3Downloads': ['relevancerank','salesrank'],
            'Music': ['psrank','salesrank','relevancerank'],
            'MusicalInstruments': ['pmrank','salesrank'],
            'MusicTracks': [''],
            'OfficeProducts': ['pmrank','salesrank','reviewrank'],
            'OutdoorLiving': ['psrank','salesrank'],
            'PCHardware': ['psrank','salesrank'],
            'PetSupplies': ['+pmrank','salesrank','relevancerank','reviewrank'],
            'Photo': ['pmrank','salesrank'],
            'Shoes': ['pmrank','relevancerank','reviewrank'],
            'Software': ['pmrank','salesrank'],
            'SportingGoods': ['relevancerank','salesrank'],
            'Tools': ['pmrank','salesrank'],
            'Toys': ['pmrank','salesrank'],
            'UnboxVideo': ['relevancerank','salesrank'],
            'VHS': ['relevancerank','salesrank'],
            'Video': ['relevancerank','salesrank'],
            'VideoGames': ['pmrank','salesrank'],
            'Watches': ['relevancerank','reviewrank','salesrank'],
            'Wireless': ['reviewrank','salesrank'],
            'WirelessAccessories': ['psrank','salesrank']}
    
    def Prettify(self, xml):
        '''Prettify'''
        soup = BeautifulSoup(xml)
        return soup.prettify()
    
    def Request(self, paramsDist):
        '''Делаем запрос'''
        paramsDist.update({'Service': 'AWSECommerceService', 'AWSAccessKeyId': self.accessKeyID, 'AssociateTag': self.assotiateTag, 'Timestamp': time.strftime('%Y-%m-%dT%H:%M:%S.000Z')})
        paramsList = sorted(paramsDist.items(), key=lambda x: x[0])
        paramsString = '&'.join([item[0] + '=' + urllib.quote(item[1]) for item in paramsList])
        stringToSign = 'GET\nwebservices.amazon.com\n/onca/xml\n' + paramsString
        signature = base64.b64encode(hmac.new(self.secretAccessKey, stringToSign, hashlib.sha256).digest())
        signedUrl = 'http://webservices.amazon.com/onca/xml?' + paramsString + '&Signature=' + urllib.quote(signature)
        response = urllib.urlopen(signedUrl).read()
        return response
    
    def BrowseNodeLookup(self, parentNodeId):
        '''Запрос BrowseNodeLookup'''
        paramsDist = {'Operation': 'BrowseNodeLookup', 'BrowseNodeId': str(parentNodeId)}
        return self.Request(paramsDist)
        
    def ItemSearch(self, keywords, page=1, searchIndex='All'):
        '''Запрос ItemSearch'''
        paramsDist = {'Operation': 'ItemSearch', 'SearchIndex': searchIndex, 'Keywords': keywords, 'ItemPage': str(page)}
        paramsDist.update({'Availability': 'Available', 'Condition': 'New', 'MinimumPrice': '1000'})
        sort = self.searchIndexesSort[searchIndex][0]
        if sort != '':
            paramsDist.update({'Sort': sort})
        return self.Request(paramsDist)

    def ItemLookup(self, itemId, responseGroups='Images,Small'):
        '''Запрос ItemSearch'''
        paramsDist = {'Operation': 'ItemLookup', 'ItemId': itemId, 'ResponseGroup': responseGroups}
        return self.Request(paramsDist)
    
    def Parse(self, keywords, count=10, searchIndex='All'):
        '''Парсим товары по кеям'''
        result = []
        pageNum = 1
        idsList = []
        count = min(count, (50 if searchIndex == 'All' else 100))
        while count > 0:
            try:
                if len(idsList) == 0:
                    print('Searching for items by keywords "%s" in "%s" ... ' % (keywords, searchIndex), end='')
                    responseSearch = self.ItemSearch(keywords, pageNum, searchIndex)
                    idsList = re.findall(r'<ASIN>([^<]*)<', responseSearch)
                    print('%d found' % len(idsList))
                    pageNum += 1
                    if len(idsList) == 0:
                        break
                itemId = idsList.pop(0)
                print('Getting information on item "%s" ... ' % itemId, end='')
                responseLookup = self.ItemLookup(itemId)
                print('ok')
                item = {}
                item['id'] = itemId
                item['title'] = re.findall(r'<Title>([^<]*)<', responseLookup, re.U)[0]
                item['imageMediumUrl'] = re.findall(r'<MediumImage><URL>([^<]*)<', responseLookup, re.U)[0]
                item['imageLargeUrl'] = re.findall(r'<LargeImage><URL>([^<]*)<', responseLookup, re.U)[0]
                item['link'] = re.findall(r'<DetailPageURL>([^<]*)<', responseLookup, re.U)[0]
                result.append(item)
                count -= 1
            except Exception as error:
                print('### Error: %s' % error)
        return result

if __name__ == '__main__':
    amazon = Amazon()
    #print(amazon.BrowseNodeLookup(2478844011))
    #print(amazon.ItemSearch('harry potter', 1, 'Books'))
    #print(amazon.ItemLookup('0062101897'))
    print(amazon.Parse('jessica', 3, 'Shoes'))
