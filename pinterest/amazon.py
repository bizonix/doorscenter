# coding=utf8
from __future__ import print_function
import os, re, sys, time, random, hmac, base64, hashlib, urllib, ConfigParser
import common

if __name__ == '__main__':
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

class Amazon(object):
    '''Парсер Амазона'''
    
    def __init__(self, printPrefix=None):
        '''Инициализация'''
        self.printPrefix = printPrefix
        config = ConfigParser.RawConfigParser()
        config.read('config.ini')
        self.accessKeyID = config.get('Amazon', 'AccessKeyID')
        self.secretAccessKey = config.get('Amazon', 'SecretAccessKey')
        self.assotiateTag = config.get('Amazon', 'AssotiateTag')
        self.departmentsList = ['All','Apparel','Appliances','ArtsAndCrafts','Automotive','Baby','Beauty','Books','Classical','DigitalMusic',
            'Grocery','DVD','Electronics','HealthPersonalCare','HomeGarden','Industrial','Jewelry','KindleStore','Kitchen','LawnAndGarden',
            'Magazines','Marketplace','Merchants','Miscellaneous','MobileApps','MP3Downloads','Music','MusicalInstruments','MusicTracks',
            'OfficeProducts','OutdoorLiving','PCHardware','PetSupplies','Photo','Shoes','Software','SportingGoods','Tools','Toys','UnboxVideo',
            'VHS','Video','VideoGames','Watches','Wireless','WirelessAccessories']
        self.departmentsSort = {'All': [''],
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
    
    def _Request(self, paramsDist):
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
        return self._Request(paramsDist)
        
    def ItemSearch(self, keywords, page=1, department='All', sortType=None):
        '''Запрос ItemSearch'''
        paramsDist = {'Operation': 'ItemSearch', 'SearchIndex': department, 'Keywords': keywords, 'ItemPage': str(page)}
        paramsDist.update({'Availability': 'Available', 'Condition': 'New', 'MinimumPrice': '1000'})
        if (sortType != None) and (sortType != ''):
            paramsDist.update({'Sort': sortType})
        return self._Request(paramsDist)

    def ItemLookup(self, itemId, responseGroups='Images,Small'):
        '''Запрос ItemLookup'''
        paramsDist = {'Operation': 'ItemLookup', 'ItemId': itemId, 'ResponseGroup': responseGroups}
        return self._Request(paramsDist)
    
    def Parse(self, keywordsList, pageNum=1, department='All', sortType=None):
        '''Парсим товары по кеям'''
        result = []
        maxPageNum = 5 if department == 'All' else 10
        if pageNum > maxPageNum:
            return result
        try:
            if sortType == None:
                sortType = random.choice(self.departmentsSort[department])
            responseSearch = self.ItemSearch(','.join(keywordsList), pageNum, department, sortType)
            itemsList = re.findall(r'<ASIN>([^<]*)<', responseSearch)
            for itemId in itemsList:
                try:
                    responseLookup = self.ItemLookup(itemId)
                    item = {}
                    item['id'] = itemId
                    item['title'] = re.findall(r'<Title>([^<]*)<', responseLookup, re.U)[0]
                    item['imageUrl'] = re.findall(r'<LargeImage><URL>([^<]*)<', responseLookup, re.U)[0]
                    item['link'] = re.findall(r'<DetailPageURL>([^<]*)<', responseLookup, re.U)[0]
                    result.append(item)
                except Exception:
                    pass
        except Exception:
            pass
        random.shuffle(result)
        return result


if (__name__ == '__main__') and common.DevelopmentMode():
    amazon = Amazon()
    print(amazon.Parse(['missoni'], 1, 'Shoes'))
