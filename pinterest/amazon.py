# coding=utf8
from __future__ import print_function
import os, re, sys, time, hmac, base64, hashlib, urllib
import common

if __name__ == '__main__':
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

class Amazon(object):
    '''Парсер Амазона'''
    
    def __init__(self, printPrefix=None):
        '''Инициализация'''
        self.printPrefix = printPrefix
        dataList = open('amazon.ini').read().splitlines()
        self.accessKeyID = dataList[0]
        self.secretAccessKey = dataList[1]
        self.assotiateTag = dataList[2]
        self.departments = ('All','Apparel','Appliances','ArtsAndCrafts','Automotive','Baby','Beauty','Books','Classical','DigitalMusic',
            'Grocery','DVD','Electronics','HealthPersonalCare','HomeGarden','Industrial','Jewelry','KindleStore','Kitchen','LawnAndGarden',
            'Magazines','Marketplace','Merchants','Miscellaneous','MobileApps','MP3Downloads','Music','MusicalInstruments','MusicTracks',
            'OfficeProducts','OutdoorLiving','PCHardware','PetSupplies','Photo','Shoes','Software','SportingGoods','Tools','Toys','UnboxVideo',
            'VHS','Video','VideoGames','Watches','Wireless','WirelessAccessories')
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
    
    def _Print(self, text, end=None):
        '''Выводим текст на консоль'''
        if self.printPrefix != None:
            text = self.printPrefix + text
            end = None  # в многопоточном режиме всегда выводим конец строки
        common.PrintThreaded(text, end)
        self.lastPrintEnd = end
    
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
        
    def ItemSearch(self, keywords, page=1, department='All'):
        '''Запрос ItemSearch'''
        paramsDist = {'Operation': 'ItemSearch', 'SearchIndex': department, 'Keywords': keywords, 'ItemPage': str(page)}
        paramsDist.update({'Availability': 'Available', 'Condition': 'New', 'MinimumPrice': '1000'})
        sort = self.departmentsSort[department][0]
        if sort != '':
            paramsDist.update({'Sort': sort})
        return self._Request(paramsDist)

    def ItemLookup(self, itemId, responseGroups='Images,Small'):
        '''Запрос ItemSearch'''
        paramsDist = {'Operation': 'ItemLookup', 'ItemId': itemId, 'ResponseGroup': responseGroups}
        return self._Request(paramsDist)
    
    def Parse(self, keywords, count=10, department='All'):
        '''Парсим товары по кеям'''
        result = []
        pageNum = 1
        idsList = []
        count = min(count, (50 if department == 'All' else 100))
        while count > 0:
            try:
                if len(idsList) == 0:
                    self._Print('Searching for items by keywords "%s" in "%s" ... ' % (keywords, department), end='')
                    responseSearch = self.ItemSearch(keywords, pageNum, department)
                    idsList = re.findall(r'<ASIN>([^<]*)<', responseSearch)
                    self._Print('%d found' % len(idsList))
                    pageNum += 1
                    if len(idsList) == 0:
                        break
                itemId = idsList.pop(0)
                self._Print('Getting information on item "%s" ... ' % itemId, end='')
                responseLookup = self.ItemLookup(itemId)
                self._Print('ok')
                item = {}
                item['id'] = itemId
                item['title'] = re.findall(r'<Title>([^<]*)<', responseLookup, re.U)[0]
                item['imageUrl'] = re.findall(r'<LargeImage><URL>([^<]*)<', responseLookup, re.U)[0]
                item['link'] = re.findall(r'<DetailPageURL>([^<]*)<', responseLookup, re.U)[0]
                result.append(item)
                count -= 1
            except Exception as error:
                self._Print('### Error: %s' % error)
        return result


if __name__ == '__main__':
    amazon = Amazon()
    print(amazon.Parse('missoni', 3, 'Shoes'))
