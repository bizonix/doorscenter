# coding=utf8
from suds import WebFault
from suds.client import Client
import xml.dom.minidom, uuid, logging

class GoDaddyAPIBase(object):
    def __init__(self, log = False):
        if log:
            logging.basicConfig(level=logging.INFO)
            logging.getLogger('suds.client').setLevel(logging.DEBUG)
        
    def _GetCltrId(self):
        '''Get GUID'''
        return str(uuid.uuid4())
    
    def _GetProductId(self, action, tld, period):
        '''Product IDs'''
        if (action == 'buy') and (tld == 'com') and (period == 1):
            return 350001
        if (action == 'buy') and (tld == 'net') and (period == 1):
            return 350030
        if (action == 'buy') and (tld == 'info') and (period == 1):
            return 350051
        if (action == 'buy') and (tld == 'biz') and (period == 2):
            return 350077
        if (action == 'buy') and (tld == 'us') and (period == 2):
            return 350127
    
    def Describe(self):
        '''The Describe method'''
        response = self.client.service.Describe(self._GetCltrId(), self.credential)
        '''Parsing request'''
        dict = {}
        dom = xml.dom.minidom.parseString(response)
        for node in dom.getElementsByTagName('resdata')[0].childNodes:
            if node.nodeType == 1:
                dict[node.nodeName] = node.childNodes[0].data
        return dict
    
    def Poll(self):
        '''The Poll method'''
        response = self.client.service.Poll(self._GetCltrId(), self.credential, 'req')
        '''Parsing request'''
        resources = []
        dom = xml.dom.minidom.parseString(response)
        for item in dom.getElementsByTagName('ITEM'):
            resources.append(item.attributes['resourceid'].value)
        return resources
        
    def Info(self, resourceId):
        '''The Info method'''
        response = self.client.service.Info(self._GetCltrId(), self.credential, resourceId)
        '''Parsing request'''
        info = {}
        dom = xml.dom.minidom.parseString(response)
        attributes = dom.getElementsByTagName('info')[0].attributes
        for n in range(attributes.length):
            info[attributes.item(n).name] = attributes.item(n).value
        return info

    def CheckAvailability(self, domains):
        '''The CheckAvailability method'''
        sDomainArray  = self.client.factory.create('ArrayOfString')
        sDomainArray.string = domains
        response = self.client.service.CheckAvailability(self._GetCltrId(), self.credential, sDomainArray)
        '''Parsing request'''
        results = {}
        dom = xml.dom.minidom.parseString(response.decode('utf-8').encode('utf-16'))
        for domainElement in dom.getElementsByTagName('domain'):
            results[domainElement.attributes['name'].value.lower()] = domainElement.attributes['avail'].value == '1'
        return results
    
    def OrderDomains(self, shopper, registrant, nexus, domains, nameServers, period):
        '''The OrderDomains method'''
        nsArray = self.client.factory.create('ArrayOfNS')
        for nameServer in nameServers:
            NS = self.client.factory.create('NS')
            NS.name = nameServer
            nsArray.NS.append(NS)
        items = self.client.factory.create('ArrayOfDomainRegistration')
        for domain in domains:
            sld, _, tld = domain.partition('.')
            order = self.client.factory.create('OrderItem')
            order.productid = self._GetProductId('buy', tld, period)
            order.quantity = 1
            order.duration = 1
            domainRegistration = self.client.factory.create('DomainRegistration')
            domainRegistration.order = order
            domainRegistration.sld = sld
            domainRegistration.tld = tld
            domainRegistration.period = period
            domainRegistration.registrant = registrant
            if tld == 'us':
                domainRegistration.nexus = nexus
            domainRegistration.nsArray = nsArray
            domainRegistration.autorenewflag = 0
            items.DomainRegistration.append(domainRegistration)
        response = self.client.service.OrderDomains(self._GetCltrId(), self.credential, shopper, items)
        '''Parsing request'''
        dom = xml.dom.minidom.parseString(response)
        userId = dom.getElementsByTagName('response')[0].attributes['user'].value
        orderId = dom.getElementsByTagName('orderid')[0].childNodes[0].data
        return userId, orderId
        
class GoDaddyAPITest(GoDaddyAPIBase):
    '''Test mode'''
    def __init__(self, log = False):
        self.url = 'https://api.ote.wildwestdomains.com/wswwdapi/wapi.asmx?wsdl'
        self.client = Client(self.url)
        self.credential = self.client.factory.create('Credential')
        self.credential.Account = '1000656'
        self.credential.Password = '43KoqW82'
        super(GoDaddyAPITest, self).__init__(log)

    def Certification(self):
        '''The certification program'''
        if self.Reset():
            '''Init'''
            print('Reset')
            resources = self.Poll()
            print('Poll: %s' % resources)
            '''Task #1. Domain Name Availability Check'''
            print('Step 1. Availability: %s' % self.CheckAvailability(['example.biz', 'example.us']))
            '''Task #2. Domain Name Registration'''
            userId1, orderId1 = self.OrderDomains(['example.biz', 'example.us'], ['ns1.example.com', 'ns2.example.com'], 2)
            print('Step 2. User1 ID: %s. Order1 ID: %s.' % (userId1, orderId1))
            domainResources = self.Poll()
            print('Poll: %s' % domainResources)
            '''Task #3. Domain Name Privacy Purchase'''
            dbpUserId1, orderId2 = self.OrderDomainPrivacy('example.biz', domainResources[0], userId1)
            print('Step 3. DBPUser1 ID: %s. Order2 ID: %s.' % (dbpUserId1, orderId2))
            dbpResources = self.Poll()
            print('Poll: %s' % dbpResources)
            '''Task #4. Domain Name Availability Check'''
            print('Step 4. Availability: %s' % self.CheckAvailability(['example.biz', 'example.us']))
            '''Task #5. Domain Name Information Query'''
            print('Step 5. Info: %s' % self.Info(domainResources[0]))
            '''Task #6. Domain Name Renewal'''
            domainResources2 = [domainResources[0], domainResources[0]]
            orderId3 = self.OrderPrivateDomainRenewals(['example.biz', 'example.us'], domainResources2, dbpResources, userId1, dbpUserId1, 'defgh')
            print('Step 6. Order3 ID: %s.' % orderId3)
            resources1 = self.Poll()
            print('Poll: %s' % resources1)
            '''Task #7. Domain Name Transfer'''
            userId2, orderId4 = self.OrderDomainTransfers('example.com')
            print('Step 7. User2 ID: %s. Order4 ID: %s.' % (userId2, orderId4))
            resources2 = self.Poll()
            print('Poll: %s' % resources2)
            '''Final'''
            print('Done')
        else:
            print('Unable to reset')
    
    def Reset(self):
        '''Reset certifcation steps'''
        request = '<wapi clTRID=\'%s\' account=\'%s\' pwd=\'%s\'><manage><script cmd=\'reset\' /></manage></wapi>' % (self._GetCltrId(), self.credential.Account, self.credential.Password)
        response = self.client.service.ProcessRequest(request)
        expectedResponse = 'scripting status reset'
        return response == expectedResponse
    
    def OrderDomains(self, domains, nameServers, period):
        '''The OrderDomains method'''
        shopper = self.client.factory.create('Shopper')
        shopper.user = 'createNew'
        shopper.pwd = 'abcde'
        shopper.email = 'agordon@wildwestdomains.com'
        shopper.firstname = 'Artemus'
        shopper.lastname = 'Gordon'
        shopper.phone = '(888)555-1212'
        registrant = self.client.factory.create('ContactInfo')
        registrant.fname = 'Artemus'
        registrant.lname = 'Gordon'
        registrant.email = 'agordon@wildwestdomains.com'
        registrant.sa1 = '2 N. Main St.'
        registrant.city = 'Valdosta'
        registrant.sp = 'Georgia'
        registrant.pc = '17123'
        registrant.cc = 'United States'
        registrant.phone = '(888)555-1212'
        nexus = self.client.factory.create('Nexus')
        nexus.category = 'citizen of US'
        nexus.use = 'personal'
        return super(GoDaddyAPITest, self).OrderDomains(shopper, registrant, nexus, domains, nameServers, period)
        
    def OrderDomainPrivacy(self, domain, resourceId, userId):
        '''The OrderDomainPrivacy method'''
        shopper = self.client.factory.create('Shopper')
        shopper.user = userId
        shopper.dbpuser = 'createNew'
        shopper.dbppwd = 'defgh'
        shopper.dbpemail = 'info@example.biz'
        order = self.client.factory.create('OrderItem')
        order.productid = 377001
        order.quantity = 1
        order.duration = 1
        dbpItems = self.client.factory.create('ArrayOfDomainByProxy')
        domainByProxy = self.client.factory.create('DomainByProxy')
        sld, _, tld = domain.partition('.')
        domainByProxy.order = order
        domainByProxy.sld = sld
        domainByProxy.tld = tld
        domainByProxy.resourceid = resourceId
        dbpItems.DomainByProxy.append(domainByProxy)
        response = self.client.service.OrderDomainPrivacy(self._GetCltrId(), self.credential, shopper, dbpItems)
        '''Parsing request'''
        dom = xml.dom.minidom.parseString(response)
        dbpUserId = dom.getElementsByTagName('response')[0].attributes['dbpuser'].value
        orderId = dom.getElementsByTagName('orderid')[0].childNodes[0].data
        return dbpUserId, orderId
    
    def OrderPrivateDomainRenewals(self, domains, domainResources, dbpResources, userId, dbpUserId, dbpUserPwd):
        '''The OrderPrivateDomainRenewals method'''
        shopper = self.client.factory.create('Shopper')
        shopper.user = userId
        shopper.dbpuser = dbpUserId
        shopper.dbppwd = dbpUserPwd
        items = self.client.factory.create('ArrayOfDomainRenewal')
        productIds = ['350087', '350137', '387001']  # for testing purposes
        for resourceId in domainResources:
            order = self.client.factory.create('OrderItem')
            order.productid = productIds[0]
            productIds = productIds[1:]  # for testing purposes
            order.quantity = 1
            order.duration = 1
            sld, _, tld = domains[0].partition('.')
            domains = domains[1:]
            domainRenewal = self.client.factory.create('DomainRenewal')
            domainRenewal.order = order
            domainRenewal.resourceid = resourceId
            domainRenewal.sld = sld
            domainRenewal.tld = tld
            domainRenewal.period = 1
            items.DomainRenewal.append(domainRenewal)
        dbpItems = self.client.factory.create('ArrayOfResourceRenewal')
        for resourceId in dbpResources:
            order = self.client.factory.create('OrderItem')
            order.productid = productIds[0]
            productIds = productIds[1:]  # for testing purposes
            order.quantity = 1
            order.duration = 1
            resourceRenewal = self.client.factory.create('ResourceRenewal')
            resourceRenewal.order = order
            resourceRenewal.resourceid = resourceId
            dbpItems.ResourceRenewal.append(resourceRenewal)
        response = self.client.service.OrderPrivateDomainRenewals(self._GetCltrId(), self.credential, shopper, items, dbpItems)
        '''Parsing request'''
        dom = xml.dom.minidom.parseString(response)
        orderId = dom.getElementsByTagName('orderid')[0].childNodes[0].data
        return orderId
    
    def OrderDomainTransfers(self, domain):
        '''The OrderDomainTransfers method'''
        shopper = self.client.factory.create('Shopper')
        shopper.user = 'createNew'
        shopper.pwd = 'ghijk'
        shopper.email = 'joe@smith.us'
        shopper.firstname = 'Joe'
        shopper.lastname = 'Smith'
        shopper.phone = '(777)555-1212'
        registrant = self.client.factory.create('ContactInfo')
        registrant.fname = 'Joe'
        registrant.lname = 'Smith'
        registrant.email = 'joe@smith.us'
        registrant.sa1 = '1 S. Main St.'
        registrant.city = 'Oakland'
        registrant.sp = 'California'
        registrant.pc = '97123'
        registrant.cc = 'United States'
        registrant.phone = '(777)555-1212'
        order = self.client.factory.create('OrderItem')
        order.productid = '350011'  # for testing purposes
        order.quantity = 1
        order.duration = 1
        sld, _, tld = domain.partition('.')
        domainTransfer = self.client.factory.create('DomainTransfer')
        domainTransfer.order = order
        domainTransfer.sld = sld
        domainTransfer.tld = tld
        items = self.client.factory.create('ArrayOfDomainTransfer')
        items.DomainTransfer.append(domainTransfer)
        response = self.client.service.OrderDomainTransfers(self._GetCltrId(), self.credential, shopper, items)
        '''Parsing request'''
        dom = xml.dom.minidom.parseString(response)
        userId = dom.getElementsByTagName('response')[0].attributes['user'].value
        orderId = dom.getElementsByTagName('orderid')[0].childNodes[0].data
        return userId, orderId

class GoDaddyAPIReal(GoDaddyAPIBase):
    '''Real mode'''
    def __init__(self, log = False):
        self.url = 'https://api.wildwestdomains.com/wswwdapi/wapi.asmx?wsdl'
        self.client = Client(self.url)
        self.credential = self.client.factory.create('Credential')
        self.credential.Account = '476475'
        self.credential.Password = 'ek6sBq2g'
        super(GoDaddyAPIReal, self).__init__(log)

    def OrderDomains(self, domains, nameServers, period):
        '''The OrderDomains method'''
        shopper = self.client.factory.create('Shopper')
        shopper.user = '46331609'
        registrant = self.client.factory.create('ContactInfo')
        registrant.fname = 'Aleksandr'
        registrant.lname = 'Borisov'
        registrant.email = 'zenstation@list.ru'
        registrant.sa1 = 'Liteiniy, 8 - 24'
        registrant.city = 'Saint Petersburg'
        registrant.sp = 'Saint Petersburg'
        registrant.pc = '191000'
        registrant.cc = 'Russian Federation'
        registrant.phone = '+7.9119456673'
        return super(GoDaddyAPIReal, self).OrderDomains(shopper, registrant, None, domains, nameServers, period)

def main():
    '''Test'''    
    #apiTest = GoDaddyAPITest(True)
    #apiTest.Certification()
    '''Real'''
    apiReal = GoDaddyAPIReal(True)
    #print(apiReal.CheckAvailability(['google.com', 'google.net', 'lasjdgaee.com']))
    apiReal.OrderDomains(['ssecure2.info'], ['ns1.ralenc.net', 'ns2.ralenc.net'], 1)
    apiReal.Poll()

if __name__ == "__main__":
    main()
