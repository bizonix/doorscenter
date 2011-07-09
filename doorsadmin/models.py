# coding=utf8
from django.db.models import Sum, Count, Max, Q
from django.db import models, transaction
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.core.mail import send_mail
from doorsadmin.common import SelectKeywords, CountKeywords, AddDomainToControlPanel, KeywordToUrl, GetFirstObject, EncodeListForAgent, DecodeListFromAgent, GenerateRandomWord, PrettyDate, GetCounter, GetPagesCounter, HtmlLinksToBBCodes, MakeListUnique, ReplaceZero
import datetime, random, re

eventTypes = (('trace', 'trace'), ('info', 'info'), ('warning', 'warning'), ('error', 'error'))
stateSimple = (('new', 'new'), ('ok', 'ok'), ('error', 'error'))
stateManaged = (('new', 'new'), ('inproc', 'inproc'), ('done', 'done'), ('error', 'error'))
languages = (('ru', 'ru'), ('en', 'en'))
encodings = (('cp1251', 'cp1251'), ('utf-8', 'utf-8'))
agentTypes = (('snippets', 'snippets'), ('doorgen', 'doorgen'), ('xrumer', 'xrumer'))
hostTypes = (('free', 'free'), ('shared', 'shared'), ('vps', 'vps'), ('real', 'real'))
hostControlPanelTypes = (('none', 'none'), ('ispconfig', 'isp config'), ('ispmanager', 'isp manager'), ('directadmin', 'direct admin'), ('cpanel', 'cpanel'))
templateTypes = (('none', 'none'), ('ddl', 'ddl'), ('redirect', 'redirect'))
taskPriorities = (('zero', 'zero'), ('std', 'std'), ('high', 'high'))

'''Helper functions'''

@transaction.commit_manually
def EventLog(type, text, object=None, addErrorMessage=None):
    '''Запись события в лог'''
    if type != 'trace':
        if addErrorMessage:
            text += ': ' + str(addErrorMessage)
        objectName = ''
        if object:
            object.lastError = text
            object.save()
            objectName = object.__class__.__name__ + ' ' + str(object)
        Event.objects.create(date=datetime.datetime.now(), 
                             type=type, 
                             object=objectName, 
                             text=text).save()
        transaction.commit()
        if type == 'error':
            send_mail('Doors Center', text + ' ' + objectName, 'alex@searchpro.name', ['alex@altstone.com'], fail_silently = True)

def ObjectLog(object, changeMessage):
    '''Запись в историю объекта'''
    LogEntry.objects.log_action(user_id = 2, content_type_id = ContentType.objects.get_for_model(object).pk,
        object_id = object.pk, object_repr = force_unicode(object), action_flag = ADDITION, 
        change_message = changeMessage)

def GetObjectByTaskType(taskType):
    '''Преобразуем имя класса в класс. Только классы-очереди для агентов'''
    if taskType == 'SnippetsSet':
        return SnippetsSet
    elif taskType == 'Doorway':
        return Doorway
    elif taskType == 'XrumerBaseR':
        return XrumerBaseR
    elif taskType == 'SpamTask':
        return SpamTask

def NextYearDate():
    '''Сегодняшняя дата плюс год'''
    return datetime.date.today() + datetime.timedelta(365)

def NextBaseNumber():
    '''Следующий номер базы'''
    return max(0, XrumerBaseRaw.objects.all().aggregate(xx=Max('baseNumber'))['xx'], XrumerBaseR.objects.all().aggregate(xx=Max('baseNumber'))['xx']) + 1

'''Abstract models'''

class BaseDoorObject(models.Model):
    '''Общие атрибуты всех объектов'''
    description = models.CharField('Description', max_length=200, default='', blank=True)
    stateSimple = models.CharField('State', max_length=50, choices = stateSimple, default='new')
    remarks = models.TextField('Remarks', default='', blank=True)
    lastError = models.CharField('Last Error', max_length=200, default='', blank=True)
    dateAdded = models.DateTimeField('Date Added', auto_now_add = True, null=True, blank=True)
    dateChanged = models.DateTimeField('Date Changed', auto_now_add = True, auto_now = True, null=True, blank=True)
    class Meta:
        abstract = True
    def __unicode__(self):
        if self.description:
            return self.description
        else:
            try:
                return '#%s \'%s\'' % (self.pk, self.niche.description)
            except Exception:
                return '#%s' % (self.pk)
    def save(self, *args, **kwargs):
        if self.stateSimple == 'new':
            self.stateSimple = 'ok'
        super(BaseDoorObject, self).save(*args, **kwargs)

class BaseDoorObjectActivatable(models.Model):
    '''Объекты, активностью которых можно управлять'''
    active = models.BooleanField('Act.', default=True)
    class Meta:
        abstract = True

class BaseDoorObjectTrackable(models.Model):
    '''Объекты, по которым нужно отслеживать статистику'''
    analyticsId = models.CharField('Analytics Id', max_length=50, default='', blank=True)
    piwikId = models.IntegerField('Piwik Id', null=True, blank=True)
    cyclikId = models.IntegerField('Cyclik Id', null=True, blank=True)
    class Meta:
        abstract = True

class BaseXrumerBase(BaseDoorObject, BaseDoorObjectActivatable):
    '''База Хрумера. File-based.'''
    baseNumber = models.IntegerField('#', unique=True, default=NextBaseNumber)
    linksCount = models.FloatField('Count, k.', null=True, blank=True)
    language = models.CharField('Language', max_length=50, choices=languages, blank=True)
    class Meta:
        abstract = True
    def __unicode__(self):
        return "#%d" % self.baseNumber

'''Real models'''

class Agent(BaseDoorObject, BaseDoorObjectActivatable):
    type = models.CharField('Agent Type', max_length=50, choices = agentTypes)
    currentTask = models.CharField('Current Task', max_length=200, default='', blank=True)
    dateLastPing = models.DateTimeField('Last Ping', null=True, blank=True)
    interval = models.IntegerField('Warning, h.', null=True, default=3)
    class Meta:
        verbose_name = 'Agent'
        verbose_name_plural = 'IV.1 # Agents - [act]'
    def GetDateLastPingAgo(self):
        return PrettyDate(self.dateLastPing)
    GetDateLastPingAgo.short_description = 'Last Ping'
    def GetQueues(self):
        '''Очереди каких объектов обрабатывает агент?'''
        if self.type == 'snippets':
            return [SnippetsSet]
        elif self.type == 'doorgen':
            return [Doorway]
        elif self.type == 'xrumer':
            return [XrumerBaseR, SpamTask]
    
'''Abstract models'''

class BaseDoorObjectManaged(models.Model):
    priority = models.CharField('Prt.', max_length=20, choices = taskPriorities, default='std')
    agent = models.ForeignKey(Agent, verbose_name='Agent', null=True, blank=True)
    runTime = models.IntegerField('Run Time', null=True)
    stateManaged = models.CharField('State', max_length=50, choices = stateManaged, default='new')
    class Meta:
        abstract = True
    def GetRunTime(self):
        '''Время выполнения'''
        try:
            return str(datetime.timedelta(0, self.runTime))
        except:
            return ''
    GetRunTime.short_description = 'Run Time'
    def GetTaskDetails(self):
        '''Подготовка данных для работы агента'''
        pass
    def SetTaskDetails(self, data):
        '''Обработка данных агента'''
        pass

class BaseDoorObjectSpammable(BaseDoorObjectManaged):
    '''Объект, по которому спамят'''
    successCount = models.IntegerField('Sc.', null=True, blank=True)
    halfSuccessCount = models.IntegerField('Hs.', null=True, blank=True)
    failsCount = models.IntegerField('Fl.', null=True, blank=True)
    profilesCount = models.IntegerField('Pr.', null=True, blank=True)
    class Meta:
        abstract = True
    def SetTaskDetails(self, data):
        '''Обработка данных агента'''
        self.successCount = data['successCount']
        self.halfSuccessCount = data['halfSuccessCount']
        self.failsCount = data['failsCount']
        self.profilesCount = data['profilesCount']
        if self.successCount * 1.0 / (self.successCount + self.halfSuccessCount + self.failsCount + 1.0) < 0.3:
            EventLog('warning', 'Too few successful posts (%d)' % self.successCount, self)

'''Real models'''

class Event(models.Model):
    '''События'''
    date = models.DateTimeField('Date', auto_now_add = True, null=True, blank=True)
    type = models.CharField('Type', max_length=50, choices=eventTypes, default='info', blank=True)
    object = models.CharField('Object', max_length=200, default='', blank=True)
    text = models.CharField('Description', max_length=1000, default='', blank=True)
    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'IV.2 Events'
    def __unicode__(self):
        return '%s: %s' % (self.type, self.text)

class Net(BaseDoorObject, BaseDoorObjectActivatable, BaseDoorObjectTrackable):
    '''Сетка доров'''
    settings = models.TextField('Settings', default='', blank=True)
    makeSpam = models.BooleanField('Spam', default=True)
    class Meta:
        verbose_name = 'Net'
        verbose_name_plural = 'I.1 # Nets - [act]'
    def GetDoorsCount(self):
        return ReplaceZero(self.domain_set.annotate(x=Count('doorway')).aggregate(xx=Sum('x'))['xx'])
    GetDoorsCount.short_description = 'Doors'
    GetDoorsCount.allow_tags = True
    def GetPagesCount(self):
        return ReplaceZero(self.domain_set.annotate(x=Sum('doorway__pagesCount')).aggregate(xx=Sum('x'))['xx'])
    GetPagesCount.short_description = 'Pages'
    GetPagesCount.allow_tags = True
    def GetDomainsCount(self):
        return GetCounter(self.domain_set, {'active': True})
    GetDomainsCount.short_description = 'Domains'
    GetDomainsCount.allow_tags = True
    def GetSchedulesCount(self):
        return GetCounter(self.doorwayschedule_set, {'active': True})
    GetSchedulesCount.short_description = 'Schedules'
    GetSchedulesCount.allow_tags = True
    def AddDomain(self, newDomain):
        '''Добавить домен в сетку'''
        newDomain.linkedDomains.clear()
        newDomain.maxLinkedDomains = random.randint(3,6)
        for domain in self.domain_set.filter(pk__lt=newDomain.pk).order_by('pk').all():  # цикл по доменам сетки до текущего
            if domain.linkedDomains.filter(pk__gt=domain.pk).count() < domain.maxLinkedDomains:
                newDomain.linkedDomains.add(domain)
                if domain.netLevel:
                    newDomain.netLevel = domain.netLevel + 1
                else:
                    newDomain.netLevel = 1
                return
        newDomain.netLevel = 1
    def GetNextDomain(self):
        '''Получить следующий свободный домен'''
        try:
            for obj in self.domain_set.filter(active=True).order_by('pk').all():
                if obj.IsRootFree():
                    return obj
            return Domain.objects.filter(Q(active=True), (Q(net=self) | Q(net=None))).order_by('?')[:1].get()
        except Exception as error:
            EventLog('error', 'Cannot find a domain', self, error)
    
class Niche(BaseDoorObject, BaseDoorObjectActivatable, BaseDoorObjectTrackable):
    '''Тематика доров'''
    language = models.CharField('Lang.', max_length=50, choices=languages)
    stopwordsList = models.TextField('Stop Words', default='', blank=True)
    tdsSchemes = models.CharField('TDS Schemes', max_length=200, default='', blank=True)
    class Meta:
        verbose_name = 'Niche'
        verbose_name_plural = 'I.2 Niches - [act]'
    def GetStopWordsCount(self):
        return len(self.stopwordsList.split('\n'))
    GetStopWordsCount.short_description = 'Stopw.'
    GetStopWordsCount.allow_tags = True
    def GetDoorsCount(self):
        return GetCounter(self.doorway_set, {'stateManaged': 'done'})
    GetDoorsCount.short_description = 'Doors'
    GetDoorsCount.allow_tags = True
    def GetPagesCount(self):
        return GetPagesCounter(self.doorway_set)
    GetPagesCount.short_description = 'Pages'
    GetPagesCount.allow_tags = True
    def GetTemplatesCount(self):
        return GetCounter(self.template_set, {'active': True}, lambda x: x <= 0 and self.active)
    GetTemplatesCount.short_description = 'Templ.'
    GetTemplatesCount.allow_tags = True
    def GetKeywordsSetsCount(self):
        return GetCounter(self.keywordsset_set, {'active': True}, lambda x: x <= 0 and self.active)
    GetKeywordsSetsCount.short_description = 'Keyw.'
    GetKeywordsSetsCount.allow_tags = True
    def GetDomainsCount(self):
        return GetCounter(self.domain_set, {'active': True}, lambda x: x <= 30 and self.active)
    GetDomainsCount.short_description = 'Domns'
    GetDomainsCount.allow_tags = True
    def GetSchedulesCount(self):
        return GetCounter(self.doorwayschedule_set, {'active': True}, lambda x: x <= 0 and self.active)
    GetSchedulesCount.short_description = 'Schd.'
    GetSchedulesCount.allow_tags = True
    def GetXrumerBasesRCount(self):
        return GetCounter(self.xrumerbaser_set, {'active': True, 'stateManaged': 'done'}, lambda x: x <= 0 and self.active)
    GetXrumerBasesRCount.short_description = 'Bas. R'
    GetXrumerBasesRCount.allow_tags = True
    def GetSnippetsSetsCount(self):
        return GetCounter(self.snippetsset_set, {'active': True}, lambda x: x <= 0 and self.active)
    GetSnippetsSetsCount.short_description = 'Snip.'
    GetSnippetsSetsCount.allow_tags = True
    def GetSpamLinksCount(self):
        n1 = SpamLink.objects.filter(~Q(spamTask=None), Q(doorway__niche=self)).count()
        n2 = SpamLink.objects.filter(Q(doorway__niche=self)).count()
        if n1 != 0:
            s1 = '%d' % n1
        else:
            s1 = '-'
        if n2 != 0:
            s2 = '%d' % n2
        else:
            s2 = '-'
        return '%s/%s' % (s1, s2)
    GetSpamLinksCount.short_description = 'Spam'
    GetSpamLinksCount.allow_tags = True
    def GetRandomTemplate(self):
        '''Получить случайный шаблон'''
        try:
            return Template.objects.filter(Q(active=True), (Q(niche=self) | Q(niche=None))).order_by('?')[:1].get()
        except Exception as error:
            EventLog('warning', 'Cannot find a template', self, error)
            return None
    def GetRandomKeywordsSet(self):
        '''Получить случайный набор ключевых слов'''
        try:
            return KeywordsSet.objects.filter(Q(active=True), (Q(niche=self) | Q(niche=None))).order_by('?')[:1].get()
        except Exception as error:
            EventLog('warning', 'Cannot find a keywords set', self, error)
            return None
    def GetRandomSnippetsSet(self):
        '''Получить случайный набор сниппетов'''
        try:
            return SnippetsSet.objects.filter(Q(active=True), (Q(niche=self) | Q(niche=None))).order_by('?')[:1].get()
        except Exception as error:
            EventLog('warning', 'Cannot find a snippets set', self, error)
            return None
    def GetRandomBaseR(self):
        '''Получить случайную базу R'''
        try:
            return XrumerBaseR.objects.filter(Q(active=True), (Q(niche=self) | Q(niche=None))).order_by('?')[:1].get()
        except Exception as error:
            EventLog('warning', 'Cannot find a base R', self, error)
            return None
    def GetNextDomain(self):
        '''Получить следующий свободный домен'''
        try:
            for obj in self.domain_set.filter(active=True).order_by('pk').all():
                if obj.IsRootFree():
                    return obj 
            return Domain.objects.filter(Q(active=True), (Q(niche=self) | Q(niche=None))).order_by('?')[:1].get()
        except Exception as error:
            EventLog('error', 'Cannot find a domain', self, error)
    def GenerateKeywordsList(self, count):
        '''Сгенерировать набор ключевых слов по теме'''
        try:
            return self.GetRandomKeywordsSet().GenerateKeywordsList(count)
        except Exception as error:
            EventLog('error', 'Cannot generate keywords list', self, error)
    def GenerateSpamTasks(self):
        '''Генерируем задания для спама. Постановка задачи:
            - ссылки для спама прогонять по базе р ниши дора; 
            - в одном задании может быть только одна база р, соответственно только одна ниша; 
            - в одном задании должно быть 3-5 разных доменов, от каждого домена 3-5 ссылок; 
            - один домен по одной базе должен прогоняться не чаще, чем через 10 прогонов.'''
        print(self)
        try:
            '''Инициализируем переменные'''
            xrumerBaseR = self.GetRandomBaseR()
            if xrumerBaseR:
                domainPositions = {}
                linksList = []  # ссылки задания
                linksLeft = 0  # сколько всего ссылок должно быть в задании
                domainsList = {}  # домены задания: домен => число ссылок от него
                domainsLeft = xrumerBaseR.nextSpamTaskDomainsCount  # сколько разных доменов надо включить в это задание
                '''Цикл по ссылкам для спама, ниша доров которых совпадает с нишей базы'''
                for spamLink in SpamLink.objects.filter(Q(spamTask=None), Q(doorway__niche=self), Q(doorway__domain__net__makeSpam=True)).order_by('?').all()[:5000]: 
                    domain = spamLink.doorway.domain
                    if domain in domainsList:  # если домен уже есть в списке
                        if domainsList[domain] <= 0:  # по домену превысили число ссылок
                            continue
                    elif domainsLeft <= 0:  # превышено число доменов
                        continue
                    else:
                        if domain not in domainPositions:  # определяем и кэшируем позицию домена
                            domainPositions[domain] = xrumerBaseR.GetDomainPosition(domain)
                        if domainPositions[domain] < 10:  # отсекаем домены, которые спамились по базе < 10 раз назад
                            continue
                        else: 
                            x = xrumerBaseR.GetSpamTaskDomainLinksCount()  # сколько ссылок в задании должно быть от этого домена, макс.
                            linksLeft += x
                            domainsList[domain] = x
                            domainsLeft -= 1
                    linksList.append(spamLink)
                    linksLeft -= 1
                    domainsList[domain] -= 1
                    '''Создаем задание'''
                    if linksLeft == 0 and domainsLeft == 0:
                        spamTask = SpamTask.objects.create(xrumerBaseR=xrumerBaseR)
                        spamTask.save()
                        for link in linksList:
                            link.spamTask = spamTask
                            link.save()
                        print('- created')
                        xrumerBaseR.nextSpamTaskDomainsCount = None
                        xrumerBaseR.save()
                        '''Инициализируем переменные'''
                        xrumerBaseR = self.GetRandomBaseR()
                        domainPositions = {}
                        linksList = []  # ссылки задания
                        linksLeft = 0  # сколько всего ссылок должно быть в задании
                        domainsList = {}  # домены задания: домен => число ссылок от него
                        domainsLeft = xrumerBaseR.nextSpamTaskDomainsCount  # сколько разных доменов надо включить в это задание
        except Exception as error:
            EventLog('trace', 'Error in GenerateSpamTasks', self, error)

class Host(BaseDoorObject):
    '''Сервер, VPS или хостинг'''
    type = models.CharField('Host Type', max_length=50, choices=hostTypes, default='shared', blank=True)
    company = models.CharField('Company', max_length=200, default='', blank=True)
    hostName = models.CharField('Host Name', max_length=200, default='', blank=True)
    costPerMonth = models.IntegerField('Cost, $', null=True, blank=True)
    diskSpace = models.IntegerField('Disk, Gb', null=True, blank=True)
    traffic = models.IntegerField('Traf., Gb', null=True, blank=True)
    controlPanelType = models.CharField('Control Panel Type', max_length=50, choices=hostControlPanelTypes, default='none', blank=True)
    controlPanelUrl = models.CharField('Control Panel URL', max_length=200, default='', blank=True)
    controlPanelServerId = models.IntegerField('Control Panel Server #', default=1, blank=True)
    rootDocumentTemplate = models.CharField('Document Path', max_length=200, default='')
    ftpLogin = models.CharField('FTP Login', max_length=200, default='', blank=True)
    ftpPassword = models.CharField('FTP Password', max_length=200, default='', blank=True)
    ftpPort = models.IntegerField('FTP Port', default=21, blank=True)
    class Meta:
        verbose_name = 'Host'
        verbose_name_plural = 'III.1 # Hosts'
    def __unicode__(self):
        return '#%s %s' % (self.pk, self.hostName)
    def GetIPAddressesCount(self):
        return self.ipaddress_set.count()
    GetIPAddressesCount.short_description = 'IP Addresses'
    GetIPAddressesCount.allow_tags = True
    def GetDomainsCount(self):
        return GetCounter(self.domain_set, {'active': True})
    GetDomainsCount.short_description = 'Domains'
    GetDomainsCount.allow_tags = True
    def GetDoorsCount(self):
        return ReplaceZero(self.domain_set.annotate(x=Count('doorway')).aggregate(xx=Sum('x'))['xx'])
    GetDoorsCount.short_description = 'Doors'
    GetDoorsCount.allow_tags = True
    def GetPagesCount(self):
        return ReplaceZero(self.domain_set.annotate(x=Sum('doorway__pagesCount')).aggregate(xx=Sum('x'))['xx'])
    GetPagesCount.short_description = 'Pages'
    GetPagesCount.allow_tags = True
    
class IPAddress(BaseDoorObject):
    '''IP адрес'''
    address = models.IPAddressField('IP Address', unique=True)
    host = models.ForeignKey(Host, verbose_name='Host', null=True, blank=True)
    class Meta:
        verbose_name = 'IP Address'
        verbose_name_plural = 'III.2 IP Addresses'
    def __unicode__(self):
        return self.address
    def GetDomainsCount(self):
        return GetCounter(self.domain_set, {'active': True})
    GetDomainsCount.short_description = 'Domains'
    GetDomainsCount.allow_tags = True
    def GetDoorsCount(self):
        return ReplaceZero(self.domain_set.annotate(x=Count('doorway')).aggregate(xx=Sum('x'))['xx'])
    GetDoorsCount.short_description = 'Doors'
    GetDoorsCount.allow_tags = True
    def GetPagesCount(self):
        return ReplaceZero(self.domain_set.annotate(x=Sum('doorway__pagesCount')).aggregate(xx=Sum('x'))['xx'])
    GetPagesCount.short_description = 'Pages'
    GetPagesCount.allow_tags = True
    
class Domain(BaseDoorObject, BaseDoorObjectActivatable):
    '''Домен'''
    name = models.CharField('Domain Name', max_length=200, unique=True)
    net = models.ForeignKey(Net, verbose_name='Net', null=True, blank=True)
    niche = models.ForeignKey(Niche, verbose_name='Niche', null=True, blank=True)
    host = models.ForeignKey(Host, verbose_name='Host', null=True)
    registrator = models.CharField('Registrator', max_length=200, default='', blank=True)
    dateRegistered = models.DateField('Registered', default=datetime.date.today, null=True, blank=True)
    dateExpires = models.DateField('Expires', default=NextYearDate, null=True, blank=True)
    ipAddress = models.ForeignKey(IPAddress, verbose_name='IP Address', null=True, blank=True)
    nameServer1 = models.CharField('Nameserver #1', max_length=200, default='', blank=True)
    nameServer2 = models.CharField('Nameserver #2', max_length=200, default='', blank=True)
    useOwnDNS = models.BooleanField('Use own DNS', default=False, blank=True)
    linkedDomains = models.ManyToManyField('self', verbose_name='Linked Domains', symmetrical=False, null=True, blank=True)
    maxLinkedDomains = models.IntegerField('Max Lnk.', null=True, blank=True)
    netLevel = models.IntegerField('Net Lvl.', null=True)
    maxDoorsCount = models.IntegerField('Max Doors', default=25)
    class Meta:
        verbose_name = 'Domain'
        verbose_name_plural = 'II.1 # Domains - [act, large]'
    def __unicode__(self):
        return '%s (%d)' % (self.name, self.pk)
    def GetDomainUrl(self):
        return '<a href="http://%s" style="color: black;">%s</a>' % (self.name, self.name)
    GetDomainUrl.short_description = 'Domain Name'
    GetDomainUrl.allow_tags = True
    def GetDoorsMaxCount(self):
        return GetCounter(self.doorway_set, {'stateManaged': 'done'}) + '/%d' % self.maxDoorsCount
    GetDoorsMaxCount.short_description = 'Doors'
    GetDoorsMaxCount.allow_tags = True
    def GetDoorsCount(self):
        return GetCounter(self.doorway_set, {'stateManaged': 'done'})
    GetDoorsCount.short_description = 'Doors'
    GetDoorsCount.allow_tags = True
    def GetPagesCount(self):
        return GetPagesCounter(self.doorway_set)
    GetPagesCount.short_description = 'Pages'
    GetPagesCount.allow_tags = True
    def GetDocumentRoot(self):
        '''Путь к корню сайта на сервере'''
        try:
            return self.host.rootDocumentTemplate % self.name
        except:
            return ''
    def IsFolderFree(self, folderName):
        '''Свободна ли указанная папка?'''
        return self.doorway_set.filter(domainFolder=folderName).count() == 0
    def IsRootFree(self):
        '''Свободен ли корень домена?'''
        return self.IsFolderFree('/')
    def GetNetLinksList(self):
        '''Получение ссылок для перелинковки'''
        linksList = []
        for domain in self.linkedDomains.filter(pk__lt=self.pk).all():
            for doorway in domain.doorway_set.filter(stateManaged='done').all():
                linksList.extend(doorway.GetSpamLinksList().split('\n'))
        return '\n'.join(MakeListUnique(linksList))
    def save(self, *args, **kwargs):
        '''Новый домен добавляем в панель управления'''
        try:
            if self.stateSimple == 'new':
                error = AddDomainToControlPanel(self.name, self.ipAddress.address, self.useOwnDNS, self.host.controlPanelType, self.host.controlPanelUrl, self.host.controlPanelServerId)
                if error != '':
                    self.lastError = error
                    self.stateSimple = 'error'
                    self.save()
        except Exception as error:
            EventLog('error', 'Cannot add domain to control panel', self, error)
        '''Если в примечании указаны еще домены, то добавляем их с теми же параметрами'''
        keyword = 'add:'
        try:
            if self.remarks.startswith(keyword):
                self.remarks = self.remarks[len(keyword):]
                for domainName in self.remarks.splitlines():
                    try:
                        Domain.objects.create(name=domainName, 
                                              net=self.net,
                                              niche=self.niche, 
                                              host=self.host, 
                                              registrator=self.registrator, 
                                              dateRegistered=self.dateRegistered, 
                                              dateExpires=self.dateExpires, 
                                              ipAddress=self.ipAddress, 
                                              nameServer1=self.nameServer1, 
                                              nameServer2=self.nameServer2, 
                                              useOwnDNS=self.useOwnDNS, 
                                              remarks='').save()
                    except Exception as error:
                        EventLog('error', 'Cannot add additional domain "%s"' % domainName, self, error)
        except Exception as error:
            EventLog('error', 'Cannot add additional domains', self, error)
        super(Domain, self).save(*args, **kwargs)
    
class Template(BaseDoorObject, BaseDoorObjectActivatable):
    '''Шаблон дора. Folder-based.'''
    type = models.CharField('Type', max_length=50, choices=templateTypes, default='none', blank=True)
    niche = models.ForeignKey(Niche, verbose_name='Niche', null=True, blank=True)
    localFolder = models.CharField('Local Folder', max_length=200, default='', blank=True)
    class Meta:
        verbose_name = 'Template'
        verbose_name_plural = 'I.4 Templates - [act]'
    def GetDoorsCount(self):
        return GetCounter(self.doorway_set, {'stateManaged': 'done'})
    GetDoorsCount.short_description = 'Doors'
    GetDoorsCount.allow_tags = True
    def GetPagesCount(self):
        return GetPagesCounter(self.doorway_set)
    GetPagesCount.short_description = 'Pages'
    GetPagesCount.allow_tags = True
    
class KeywordsSet(BaseDoorObject, BaseDoorObjectActivatable):
    '''Набор ключевых слов. Folder-based.'''
    niche = models.ForeignKey(Niche, verbose_name='Niche', null=True)
    localFolder = models.CharField('Local Folder', max_length=200, default='')
    encoding = models.CharField('Encoding', max_length=50, choices=encodings, default='cp1251')
    keywordsCount = models.FloatField('Keys Count, k.', null=True, blank=True)
    class Meta:
        verbose_name = 'Keywords Set'
        verbose_name_plural = 'I.3 Keywords Sets - [act]'
    def GetLocalFolder(self):
        s = self.localFolder
        s = s.replace('/home/admin/public_html/searchpro.name/web/doorscenter/keywords/', '.../')
        return s
    GetLocalFolder.short_description = 'Local Folder'
    GetLocalFolder.allow_tags = True
    def GetDoorsCount(self):
        return GetCounter(self.doorway_set, {'stateManaged': 'done'})
    GetDoorsCount.short_description = 'Doors'
    GetDoorsCount.allow_tags = True
    def GetPagesCount(self):
        return GetPagesCounter(self.doorway_set)
    GetPagesCount.short_description = 'Pages'
    GetPagesCount.allow_tags = True
    def GenerateKeywordsList(self, count):
        '''Сгенерировать набор ключевых слов по теме'''
        try:
            return SelectKeywords(self.localFolder, self.encoding, count)
        except Exception as error:
            EventLog('error', 'Cannot generate keywords list', self, error)
    def save(self, *args, **kwargs):
        '''Если не указано число ключей, то считаем их'''
        try:
            if self.keywordsCount == None:
                self.keywordsCount = CountKeywords(self.localFolder) / 1000.0
        except Exception as error:
            EventLog('error', 'Cannot count keywords list', self, error)
        super(KeywordsSet, self).save(*args, **kwargs)

class DoorgenProfile(BaseDoorObject, BaseDoorObjectActivatable):
    '''Профиль доргена'''
    settings = models.TextField('Settings', default='')
    class Meta:
        verbose_name = 'Doorgen Profile'
        verbose_name_plural = 'III.3 Profiles - [act]'
    def GetDoorsCount(self):
        return GetCounter(self.doorway_set, {'stateManaged': 'done'})
    GetDoorsCount.short_description = 'Doors'
    GetDoorsCount.allow_tags = True
    def GetPagesCount(self):
        return GetPagesCounter(self.doorway_set)
    GetPagesCount.short_description = 'Pages'
    GetPagesCount.allow_tags = True
    
class DoorwaySchedule(BaseDoorObject, BaseDoorObjectActivatable):
    '''Менеджер генерации дорвеев'''
    net = models.ForeignKey(Net, verbose_name='Net', null=True)
    niche = models.ForeignKey(Niche, verbose_name='Niche', null=True)
    template = models.ForeignKey(Template, verbose_name='Template', null=True, blank=True)
    keywordsSet = models.ForeignKey(KeywordsSet, verbose_name='Kwrds Set', null=True, blank=True)
    doorgenProfile = models.ForeignKey(DoorgenProfile, verbose_name='Prof.', null=True)
    minPagesCount = models.IntegerField('Min Pgs', null=True, default=500)
    maxPagesCount = models.IntegerField('Max Pgs', null=True, default=900)
    minSpamLinksPercent = models.FloatField('Min Lnk, %', default=4)
    maxSpamLinksPercent = models.FloatField('Max Lnk, %', default=5)
    dateStart = models.DateField('Start Date', null=True, blank=True, default=datetime.date.today)
    dateEnd = models.DateField('End Date', null=True, blank=True)
    doorsPerDay = models.IntegerField('Drs/Day', null=True, default=1)
    lastRun = models.DateTimeField('Last Run Date', null=True)
    doorsToday = models.IntegerField('Drs ths Day', null=True, default=0)
    class Meta:
        verbose_name = 'Schedule'
        verbose_name_plural = 'I.5 Schedules - [act]'
    def GetDoorsTodayCount(self):
        return '%d/%d' % (self.doorsToday, self.doorsPerDay)
    GetDoorsTodayCount.short_description = 'Today'
    GetDoorsTodayCount.allow_tags = True
    def GetDoorsCount(self):
        return GetCounter(self.doorway_set, {'stateManaged': 'done'})
    GetDoorsCount.short_description = 'Doors'
    GetDoorsCount.allow_tags = True
    def GetPagesCount(self):
        return GetPagesCounter(self.doorway_set)
    GetPagesCount.short_description = 'Pages'
    GetPagesCount.allow_tags = True
    def _NewDayCome(self):
        '''Настали новые сутки по сравнению с lastRun?'''
        try:
            return datetime.datetime.now().strftime('%d.%m.%Y') != self.lastRun.strftime('%d.%m.%Y')
        except:
            return True
    def _GenerateDoorwaysPrivate(self, count):
        '''Генерируем дорвей'''
        if count > 0:
            for _ in range(0, count):
                try:
                    p = Doorway.objects.create(niche=self.niche, 
                                               template=self.template, 
                                               keywordsSet=self.keywordsSet, 
                                               doorgenProfile=self.doorgenProfile, 
                                               domain=self.net.GetNextDomain(), 
                                               pagesCount=random.randint(self.minPagesCount, self.maxPagesCount), 
                                               domainFolder='', 
                                               spamLinksCount=0, 
                                               doorwaySchedule=self)
                    '''Число ссылок для спама задается в процентах, 
                    а в абсолютных числах должно быть не меньше трех и не больше страниц дора'''
                    p.spamLinksCount = min(p.pagesCount, max(3, int(p.pagesCount * random.uniform(self.minSpamLinksPercent, self.maxSpamLinksPercent) / 100.0)))
                    p.save()
                except Exception as error:
                    EventLog('error', 'Cannot generate dorway', self, error)
        
    def GenerateDoorways(self, count = None):
        '''Определяем сколько дорвеев надо сгенерировать и генерируем'''
        try:
            if count == None:  # число дорвеев не задано, определяем сами
                if self._NewDayCome():  # если настал новый день
                    if self.doorsToday > 0:  # генерим оставшиеся дорвеи за вчера, если вчера был сгенерирован хотя бы один дорвей
                        self._GenerateDoorwaysPrivate(self.doorsPerDay - self.doorsToday)
                    self.doorsToday = 0  # обнуляем число сгенерированных за сегодня дорвеев
                d = datetime.datetime.now()
                count = int(round(self.doorsPerDay * (d.hour * 60.0 + d.minute) / (24 * 60))) - self.doorsToday
            elif self._NewDayCome():  # если число задано и настал новый день
                self.doorsToday = 0  # обнуляем число сгенерированных за сегодня дорвеев
            self._GenerateDoorwaysPrivate(count)  # генерим дорвеи за сегодня
            self.lastRun = datetime.datetime.now()  # обновляем статистику
            self.doorsToday += count
        except Exception as error:
            EventLog('error', 'Cannot generate dorways', self, error)
        self.save()
        
class SpamLink(models.Model):
    '''Ссылки для спама'''
    url = models.CharField('URL', max_length = 1000, default = '')
    anchor = models.CharField('Anchor', max_length = 1000, default = '')
    doorway = models.ForeignKey('Doorway', verbose_name='Doorway')
    spamTask = models.ForeignKey('SpamTask', verbose_name='Spam Task', null=True, blank=True)
    class Meta:
        verbose_name = 'Spam Link'
        verbose_name_plural = 'II.3 Spam Links - [large]'
    def IsAssigned(self):
        return self.spamTask != None
    IsAssigned.short_description = 'Ass.'
    
class Doorway(BaseDoorObject, BaseDoorObjectTrackable, BaseDoorObjectManaged):
    '''Дорвей'''
    niche = models.ForeignKey(Niche, verbose_name='Niche', null=True)
    template = models.ForeignKey(Template, verbose_name='Template', null=True, blank=True)
    keywordsSet = models.ForeignKey(KeywordsSet, verbose_name='Kwrds Set', null=True, blank=True)
    doorgenProfile = models.ForeignKey(DoorgenProfile, verbose_name='Prof.', null=True)
    pagesCount = models.IntegerField('Pgs', null=True)
    domain = models.ForeignKey(Domain, verbose_name='Domain', null=True, blank=True)
    domainFolder = models.CharField('Domain Folder', max_length=200, default='', blank=True)
    spamLinksCount = models.IntegerField('Lnks', null=True)
    doorwaySchedule = models.ForeignKey(DoorwaySchedule, verbose_name='Schedule', null=True, blank=True)
    keywordsList = models.TextField('Keywords List', default='', blank=True)
    netLinksList = models.TextField('Net Links', default='', blank=True)  # ссылки сетки для линковки этого дорвея
    class Meta:
        verbose_name = 'Doorway'
        verbose_name_plural = 'II.2 Doorways - [large, managed]'
    def GetNet(self):
        return self.domain.net
    GetNet.short_description = 'Net'
    def GetTemplateType(self):
        return self.template.type
    GetTemplateType.short_description = 'Template Type'
    def GetUrl(self):
        return '<a href="http://%s%s">%s</a>' % (self.domain.name, self.domainFolder, self.domain.name) 
    GetUrl.short_description = 'Link'
    GetUrl.allow_tags = True
    def GetSpamLinksCount(self):
        n1 = SpamLink.objects.filter(Q(doorway=self), ~Q(spamTask=None)).count()
        if n1 != 0:
            s1 = '%d' % n1
        else:
            s1 = '-'
        return '%s/%d' % (s1, self.spamLinksCount)
    GetSpamLinksCount.short_description = 'Lnks'
    GetSpamLinksCount.allow_tags = True
    def GetSpamLinksList(self):
        '''Получаем список ссылок для спама'''
        s = ''
        for spamLink in SpamLink.objects.filter(doorway=self):
            s += '<a href="%s">%s</a>\n' % (spamLink.url, spamLink.anchor)
        return s
    def GetTaskDetails(self):
        '''Подготовка данных для работы агента'''
        if self.netLinksList == '':
            self.netLinksList = self.domain.GetNetLinksList()
        return({
                'keywordsList': EncodeListForAgent(self.keywordsList), 
                'templateFolder': self.template.localFolder, 
                'doorgenSettings': EncodeListForAgent(self.doorgenProfile.settings), 
                'domain': self.domain.name, 
                'domainFolder': self.domainFolder, 
                'netLinksList': EncodeListForAgent(self.netLinksList),
                'analyticsId': self.analyticsId,
                'piwikId': self.piwikId,
                'cyclikId': self.cyclikId,
                'documentRoot': self.domain.GetDocumentRoot(), 
                'ftpHost': self.domain.ipAddress.address, 
                'ftpLogin': self.domain.host.ftpLogin, 
                'ftpPassword': self.domain.host.ftpPassword, 
                'ftpPort': self.domain.host.ftpPort})
    def SetTaskDetails(self, data):
        '''Обработка данных агента'''
        rxHtml = re.compile(r'<a href="(.*)">(.*)</a>')
        SpamLink.objects.filter(doorway=self).delete()
        for link in DecodeListFromAgent(data['spamLinksList'][:self.spamLinksCount]).split('\n'):
            '''Парсим'''
            link = link.strip()
            x = rxHtml.match(link)
            if not x:
                continue
            if len(x.groups()) != 2:
                continue
            url = x.groups()[0]
            anchor = x.groups()[1]
            '''Создаем ссылки'''
            SpamLink.objects.create(url=url, anchor=anchor, doorway=self).save()
            if url.endswith('/index.html'):
                url = url.replace('/index.html', '/sitemap.html')
                SpamLink.objects.create(url=url, anchor=anchor, doorway=self).save()
    def save(self, *args, **kwargs):
        '''Если не указаны шаблон или набор кеев - берем случайные по нише'''
        if self.template == None:
            self.template = self.niche.GetRandomTemplate()
        if self.keywordsSet == None:
            self.keywordsSet = self.niche.GetRandomKeywordsSet()
        '''Если не указан домен - берем следующий свободный по нише'''
        if self.domain == None:
            self.domain = self.niche.GetNextDomain()
        '''Если нет ключевых слов, то генерируем'''
        if self.keywordsList == '':
            self.keywordsList = '\n'.join(self.keywordsSet.GenerateKeywordsList(self.pagesCount))
        '''Если нет ссылок сетки, то генерируем'''
        if self.netLinksList == '':
            self.netLinksList = self.domain.GetNetLinksList()
        '''Если не указаны tracking fields, то заполняем по сети и нише (приоритет: net, niche).'''
        try:
            if self.analyticsId == '':
                self.analyticsId = self.domain.net.analyticsId
        except Exception:
            pass
        try:
            if self.analyticsId == '':
                self.analyticsId = self.niche.analyticsId
        except Exception:
            pass
        try:
            self.piwikId = GetFirstObject([self.piwikId, self.domain.net.piwikId, self.niche.piwikId])
        except Exception:
            pass
        try:
            self.cyclikId = GetFirstObject([self.cyclikId, self.domain.net.cyclikId, self.niche.cyclikId])
        except Exception:
            pass
        '''Если не указана папка домена, то пытаемся занять корень. Если не получается,
        то придумываем новую папку по названию первого кея из списка'''
        if self.domainFolder == '':
            if self.domain.IsRootFree():
                self.domainFolder = r'/'
            else:
                self.domainFolder = r'/' + KeywordToUrl(self.keywordsList[:self.keywordsList.find('\n')])
        '''Если у домена не указана ниша, то устанавливаем ее'''
        if self.domain.niche == None:
            self.domain.niche = self.niche
            self.domain.save()
        '''Если на домене превышено максимальное количество доров, то отключаем домен'''
        if self.domain.doorway_set.count() >= self.domain.maxDoorsCount:
            self.domain.active = False
            self.domain.save()
        super(Doorway, self).save(*args, **kwargs)

class SnippetsSet(BaseDoorObject, BaseDoorObjectActivatable, BaseDoorObjectManaged):
    '''Сниппеты'''
    niche = models.ForeignKey(Niche, verbose_name='Niche', null=True)
    localFile = models.CharField('Local File', max_length=200, default='')
    keywordsCount = models.IntegerField('Keywords', null=True, default=500)
    interval = models.IntegerField('Interval, h.', null=True, default=100)
    dateLastParsed = models.DateTimeField('Last Parsed', null=True, blank=True)
    phrasesCount = models.IntegerField('Count', null=True, blank=True)
    class Meta:
        verbose_name = 'Snippets Set'
        verbose_name_plural = 'I.6 Snippets Sets - [act, managed]'
    def GetDateLastParsedAgo(self):
        return PrettyDate(self.dateLastParsed)
    GetDateLastParsedAgo.short_description = 'Last Parsed'
    def GetTaskDetails(self):
        '''Подготовка данных для работы агента'''
        return({'localFile': self.localFile, 
                'keywordsList': EncodeListForAgent('\n'.join(self.niche.GenerateKeywordsList(self.keywordsCount))), 
                'stopwordsList': EncodeListForAgent(self.niche.stopwordsList), 
                'language': self.niche.language})
    def SetTaskDetails(self, data):
        '''Обработка данных агента'''
        self.phrasesCount = data['phrasesCount'] 
        self.dateLastParsed = datetime.datetime.now()
        if self.phrasesCount <= 5000:
            EventLog('warning', 'Too few snippets found (%d)' % self.phrasesCount, self)

class XrumerBaseRaw(BaseXrumerBase):
    '''Сырая база Хрумера. File-based.'''
    class Meta:
        verbose_name = 'Xrumer Base Raw'
        verbose_name_plural = 'III.4 Xrumer Bases Raw - [act]'
    def GetXrumerBasesRCount(self):
        return GetCounter(self.xrumerbaser_set, {'active': True, 'stateManaged': 'done'})
    GetXrumerBasesRCount.short_description = 'Bases R'
    GetXrumerBasesRCount.allow_tags = True

class XrumerBaseR(BaseXrumerBase, BaseDoorObjectSpammable):
    '''База R для Хрумера. File-based.'''
    niche = models.ForeignKey(Niche, verbose_name='Niche', null=True)
    xrumerBaseRaw = models.ForeignKey(XrumerBaseRaw, verbose_name='Base Raw', null=True)
    snippetsSet = models.ForeignKey(SnippetsSet, verbose_name='Snippets', null=True, blank=True)
    nickName = models.CharField('Nick Name', max_length=200, default='')
    realName = models.CharField('Real Name', max_length=200, default='')
    password = models.CharField('Password', max_length=200, default='')
    emailAddress = models.CharField('E.Address', max_length=200, default='niiokr2012@gmail.com')
    emailLogin = models.CharField('E.Login', max_length=200, default='niiokr2012@gmail.com')
    emailPassword = models.CharField('E.Password', max_length=200, default='kernel32')
    emailPopServer = models.CharField('E.Pop Server', max_length=200, default='pop.gmail.com')
    spamTaskDomainsMin = models.IntegerField('Spam Task Domains Min', default = 3)
    spamTaskDomainsMax = models.IntegerField('Spam Task Domains Max', default = 5)
    nextSpamTaskDomainsCount = models.IntegerField('...', default = 4)
    spamTaskDomainLinksMin = models.IntegerField('Spam Task Domain Links Min', default = 3)
    spamTaskDomainLinksMax = models.IntegerField('Spam Task Domain Links Max', default = 5)
    class Meta:
        verbose_name = 'Xrumer Base R'
        verbose_name_plural = 'I.7 Xrumer Bases R - [act, managed]'
    def GetSpamTasksCount(self):
        return GetCounter(self.spamtask_set, {'stateManaged': 'done'})
    GetSpamTasksCount.short_description = 'Spam'
    GetSpamTasksCount.allow_tags = True
    def GetSpamTaskDomainLinksCount(self):
        return random.randint(self.spamTaskDomainLinksMin, self.spamTaskDomainLinksMax)
    def GetDomainPosition(self, domain):
        '''Как давно домен спамился по этой базе'''
        n = 1
        for spamTask in self.spamtask_set.order_by('-pk').all():
            for spamLink in spamTask.spamlink_set.all():
                if spamLink.doorway.domain == domain:
                    EventLog('trace', 'Domain position: %d' % n)
                    return n
            n += 1
            if n > 10:  # дальше проверять не надо
                return 1000
        EventLog('trace', 'Domain position: %d' % 1000)
        return 1000
    def GetTaskDetailsCommon(self):
        '''Подготовка данных для работы агента - общая часть для задания на спам'''
        return {'baseNumber': self.xrumerBaseRaw.baseNumber,  # база, по которой спамим. в случае создания базы R здесь указывается номер сырой базы, в случае спама по базе R здесь указывается номер базы R
                'baseNumberDest': self.baseNumber,  # в случае создания базы R здесь указывается номер, присваемый созданной базе, в случае спама по базе R параметр не имеет значения
                'nickName': self.nickName, 
                'realName': self.realName, 
                'password': self.password, 
                'emailAddress': self.emailAddress.replace('@gmail.com', '+%s@gmail.com' % self.nickName), 
                'emailPassword': self.emailPassword, 
                'emailLogin': self.emailLogin, 
                'emailPopServer': self.emailPopServer, 
                'snippetsFile': self.snippetsSet.localFile,
                'spamLinksList': [],
                'subjectsList': []}
    def GetTaskDetails(self):
        '''Подготовка данных для работы агента'''
        result = self.GetTaskDetailsCommon()
        result['subjectsList'] = self.niche.GenerateKeywordsList(5000)
        return result
    def SetTaskDetails(self, data):
        '''Обработка данных агента'''
        if data['rBaseLinksCount'] != 0:
            self.linksCount = data['rBaseLinksCount'] / 1000.0
        super(XrumerBaseR, self).SetTaskDetails(data)
    def save(self, *args, **kwargs):
        '''Если не указан набор сниппетов - берем случайные по нише'''
        if self.snippetsSet == None:
            self.snippetsSet = self.niche.GetRandomSnippetsSet()
        '''Если не указаны ник, имя и пароль - генерим случайные'''
        if self.nickName == '':
            self.nickName = '#gennick[%s]' % GenerateRandomWord(12).upper()
        if self.realName == '':
            self.realName = '#gennick[%s]' % GenerateRandomWord(12).upper()
        if self.password == '':
            self.password = GenerateRandomWord(12)
        '''Сколько доменов должно включать в себя следующее задание для спама по этой базе'''
        if self.nextSpamTaskDomainsCount == None:
            self.nextSpamTaskDomainsCount = random.randint(self.spamTaskDomainsMin, self.spamTaskDomainsMax)
        super(XrumerBaseR, self).save(*args, **kwargs)
    
class SpamTask(BaseDoorObject, BaseDoorObjectSpammable):
    '''Задание на спам'''
    xrumerBaseR = models.ForeignKey(XrumerBaseR, verbose_name='Base R', null=True)
    snippetsSet = models.ForeignKey(SnippetsSet, verbose_name='Snippets', null=True, blank=True)
    class Meta:
        verbose_name = 'Spam Task'
        verbose_name_plural = 'II.4 Spam Tasks - [large, managed]'
    def GetSpamLinksList(self):
        '''Получаем список ссылок для спама'''
        s = ''
        for spamLink in SpamLink.objects.filter(spamTask=self):
            s += '<a href="%s">%s</a>\n' % (spamLink.url, spamLink.anchor)
        return s
    def GetTaskDetails(self):
        '''Подготовка данных для работы агента'''
        result = self.xrumerBaseR.GetTaskDetailsCommon()  # берем общую информацию из базы R
        result['baseNumber'] = self.xrumerBaseR.baseNumber  # перезаписываем нужные параметры
        result['snippetsFile'] = self.snippetsSet.localFile
        result['spamLinksList'] = HtmlLinksToBBCodes(EncodeListForAgent(self.GetSpamLinksList()))
        return result
    def SetTaskDetails(self, data):
        '''Обработка данных агента'''
        if data['rBaseLinksCount'] != 0:
            self.xrumerBaseR.linksCount = data['rBaseLinksCount'] / 1000.0
            self.xrumerBaseR.save()
        super(SpamTask, self).SetTaskDetails(data)
    def save(self, *args, **kwargs):
        '''Если не указан набор сниппетов - берем случайные по нише базы'''
        if self.snippetsSet == None:
            self.snippetsSet = self.xrumerBaseR.niche.GetRandomSnippetsSet()
        super(SpamTask, self).save(*args, **kwargs)
