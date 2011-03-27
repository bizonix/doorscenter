# coding=utf8
from django.db.models import Sum, Count, Q
from django.db import models, transaction
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from doorsadmin.common import *
import os, datetime, random, codecs

eventTypes = (('trace', 'trace'), ('info', 'info'), ('warning', 'warning'), ('error', 'error'))
stateSimple = (('new', 'new'), ('ok', 'ok'), ('error', 'error'))
stateManaged = (('new', 'new'), ('inproc', 'inproc'), ('done', 'done'), ('error', 'error'))
languages = (('ru', 'ru'), ('en', 'en'))
encodings = (('utf-8', 'utf-8'), ('cp1251', 'cp1251'))
agentTypes = (('doorgen', 'doorgen'), ('xrumer', 'xrumer'), ('snippets', 'snippets'))
hostTypes = (('free', 'free'), ('shared', 'shared'), ('vps', 'vps'), ('real', 'real'))
hostControlPanelTypes = (('none', 'none'), ('ispconfig', 'isp config'), ('ispmanager', 'isp manager'), ('directadmin', 'direct admin'), ('cpanel', 'cpanel'))
templateTypes = (('none', 'none'), ('ddl', 'ddl'), ('redirect', 'redirect'))

'''Helper functions'''

@transaction.commit_manually
def EventLog(type, text, object=None, error=None):
    '''Запись события в лог'''
    if error:
        text += ': ' + str(error)
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

def ObjectLog(object, changeMessage):
    '''Запись в историю объекта'''
    LogEntry.objects.log_action(user_id = 2, content_type_id = ContentType.objects.get_for_model(object).pk,
        object_id = object.pk, object_repr = force_unicode(object), action_flag = ADDITION, 
        change_message = changeMessage)

def GetObjectByTaskType(taskType):
    '''Преобразуем имя класса в класс. Только классы-очереди для агентов'''
    if taskType == 'Doorway':
        return Doorway
    elif taskType == 'XrumerBaseRaw':
        return XrumerBaseRaw
    elif taskType == 'SpamTask':
        return SpamTask
    elif taskType == 'SnippetsSet':
        return SnippetsSet

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
        return '#%s %s' % (self.pk, self.description)
    def save(self, *args, **kwargs):
        if self.stateSimple == 'new':
            self.stateSimple = 'ok'
        super(BaseDoorObject, self).save(*args, **kwargs)

class BaseDoorObjectActivatable(models.Model):
    '''Объекты, активностью которых можно управлять'''
    active = models.BooleanField('Active', default=True)
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
    baseNumber = models.IntegerField('Base Number', unique=True)
    localFile = models.CharField('Local File', max_length=200, null=True, blank=True)  
    class Meta:
        abstract = True
    def __unicode__(self):
        return "Base #%d" % self.baseNumber

'''Real models'''

class Agent(BaseDoorObject, BaseDoorObjectActivatable):
    type = models.CharField('Agent Type', max_length=50, choices = agentTypes)
    currentTask = models.CharField('Current Task', max_length=200, default='', blank=True)
    dateLastPing = models.DateTimeField('Last Ping', null=True, blank=True)
    interval = models.IntegerField('Warning Interval, h.', null=True, default=3)
    class Meta:
        verbose_name = 'Agent'
        verbose_name_plural = '1. Agents'
    def GetQueues(self):
        '''Очереди каких объектов обрабатывает агент?'''
        if self.type == 'doorgen':
            return [Doorway]
        elif self.type == 'xrumer':
            return [SpamTask, XrumerBaseRaw]
        elif self.type == 'snippets':
            return [SnippetsSet]
    
'''Abstract models'''

class BaseDoorObjectManaged(models.Model):
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

'''Real models'''

class Event(models.Model):
    '''События'''
    date = models.DateTimeField('Date', auto_now_add = True, null=True, blank=True)
    type = models.CharField('Type', max_length=50, choices=eventTypes, default='info', blank=True)
    object = models.CharField('Object', max_length=200, default='', blank=True)
    text = models.CharField('Description', max_length=1000, default='', blank=True)
    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = '1.1. Events - @big'
    def __unicode__(self):
        return '%s: %s' % (self.type, self.text)

class Niche(BaseDoorObject, BaseDoorObjectActivatable, BaseDoorObjectTrackable):
    '''Тематика доров'''
    language = models.CharField('Language', max_length=50, choices=languages)
    stopwordsList = models.TextField('Stop Words', default='', blank=True)
    tdsSchemes = models.CharField('TDS Schemes', max_length=200, default='', blank=True)
    class Meta:
        verbose_name = 'Niche'
        verbose_name_plural = '3.1. Niches'
    def __unicode__(self):
        return '#%s %s (%s)' % (self.pk, self.description, self.language)
    def GetDoorsCount(self):
        return self.doorway_set.count()
    GetDoorsCount.short_description = 'Doors'
    def GetPagesCount(self):
        return self.doorway_set.aggregate(x=Sum('pagesCount'))['x']
    GetPagesCount.short_description = 'Pages'
    def GetTemplatesCount(self):
        return self.template_set.count()
    GetTemplatesCount.short_description = 'Templates'
    def GetKeywordsSetsCount(self):
        return self.keywordsset_set.count()
    GetKeywordsSetsCount.short_description = 'Keywords Sets'
    def GetDomainsCount(self):
        return self.domain_set.count()
    GetDomainsCount.short_description = 'Domains'
    def GetXrumerBasesRCount(self):
        return self.xrumerbaser_set.count()
    GetXrumerBasesRCount.short_description = 'R-Bases'
    def GetSpamTasksCount(self):
        return self.spamtask_set.count()
    GetSpamTasksCount.short_description = 'Spam Tasks'
    def GetSnippetsSetsCount(self):
        return self.snippetsset_set.count()
    GetSnippetsSetsCount.short_description = 'Snippets Sets'
    def GetRandomTemplate(self):
        '''Получить случайный шаблон'''
        try:
            return Template.objects.filter(Q(active=True), (Q(niche=self) | Q(niche=None))).order_by('?')[:1].get()
        except Exception as error:
            EventLog('error', 'Cannot find template', self, error)
    def GetRandomKeywordsSet(self):
        '''Получить случайный набор ключевых слов'''
        try:
            return KeywordsSet.objects.filter(Q(active=True), Q(niche=self)).order_by('?')[:1].get()
        except Exception as error:
            EventLog('error', 'Cannot find keywords set', self, error)
    def GetRandomDomain(self):
        '''Получить случайный домен'''
        try:
            return Domain.objects.filter(Q(active=True), (Q(niche=self) | Q(niche=None))).order_by('?')[:1].get()
        except Exception as error:
            EventLog('error', 'Cannot find domain', self, error)
    def GenerateKeywordsList(self, count):
        '''Сгенерировать набор ключевых слов по теме'''
        try:
            return self.GetRandomKeywordsSet().GenerateKeywordsList(count)
        except Exception as error:
            EventLog('error', 'Cannot generate keywords list', self, error)

class Host(BaseDoorObject):
    '''Сервер, VPS или хостинг'''
    type = models.CharField('Host Type', max_length=50, choices=hostTypes, default='shared', blank=True)
    company = models.CharField('Company', max_length=200, default='', blank=True)
    hostName = models.CharField('Host Name', max_length=200, default='', blank=True)
    costPerMonth = models.IntegerField('Cost per Month, $', null=True, blank=True)
    diskSpace = models.IntegerField('Disk Space, Gb', null=True, blank=True)
    traffic = models.IntegerField('Traffic, Gb/m', null=True, blank=True)
    controlPanelType = models.CharField('Control Panel Type', max_length=50, choices=hostControlPanelTypes, default='none', blank=True)
    controlPanelUrl = models.CharField('Control Panel URL', max_length=200, default='', blank=True)
    rootDocumentTemplate = models.CharField('Document Path', max_length=200, default='')
    ftpLogin = models.CharField('FTP Login', max_length=200, default='', blank=True)
    ftpPassword = models.CharField('FTP Password', max_length=200, default='', blank=True)
    ftpPort = models.IntegerField('FTP Port', default=21, blank=True)
    class Meta:
        verbose_name = 'Host'
        verbose_name_plural = '2.1. Hosts'
    def __unicode__(self):
        return '%s #%s %s' % (self.__class__.__name__, self.pk, self.company + ' - ' + self.hostName)
    def GetIPAddressesCount(self):
        return self.ipaddress_set.count()
    GetIPAddressesCount.short_description = 'IP Addresses'
    def GetDomainsCount(self):
        return self.domain_set.count()
    GetDomainsCount.short_description = 'Domains'
    def GetDoorsCount(self):
        return self.domain_set.annotate(x=Count('doorway')).aggregate(xx=Sum('x'))['xx']
    GetDoorsCount.short_description = 'Doors'
    def GetPagesCount(self):
        return self.domain_set.annotate(x=Sum('doorway__pagesCount')).aggregate(xx=Sum('x'))['xx']
    GetPagesCount.short_description = 'Pages'
    
class IPAddress(BaseDoorObject):
    '''IP адрес'''
    address = models.IPAddressField('IP Address')
    host = models.ForeignKey(Host, verbose_name='Host', null=True, blank=True)
    class Meta:
        verbose_name = 'IP Address'
        verbose_name_plural = '2.2. IP Addresses'
    def __unicode__(self):
        return self.address
    def GetDomainsCount(self):
        return self.domain_set.count()
    GetDomainsCount.short_description = 'Domains'
    def GetDoorsCount(self):
        return self.domain_set.annotate(x=Count('doorway')).aggregate(xx=Sum('x'))['xx']
    GetDoorsCount.short_description = 'Doors'
    def GetPagesCount(self):
        return self.domain_set.annotate(x=Sum('doorway__pagesCount')).aggregate(xx=Sum('x'))['xx']
    GetPagesCount.short_description = 'Pages'
    
class Domain(BaseDoorObject, BaseDoorObjectActivatable):
    '''Домен'''
    name = models.CharField('Domain Name', max_length=200)
    niche = models.ForeignKey(Niche, verbose_name='Niche', null=True, blank=True)
    host = models.ForeignKey(Host, verbose_name='Host', null=True)
    registrator = models.CharField('Registrator', max_length=200, default='', blank=True)
    dateRegistered = models.DateField('Date Registered', null=True, blank=True)
    dateExpires = models.DateField('Date Expires', null=True, blank=True)
    ipAddress = models.ForeignKey(IPAddress, verbose_name='IP Address', null=True, blank=True)
    nameServer1 = models.CharField('Nameserver #1', max_length=200, default='', blank=True)
    nameServer2 = models.CharField('Nameserver #2', max_length=200, default='', blank=True)
    maxDoorsCount = models.IntegerField('Max Doors', default=25)
    class Meta:
        verbose_name = 'Domain'
        verbose_name_plural = '2. Domains - @big'
    def __unicode__(self):
        return self.name
    def GetDoorsCount(self):
        return self.doorway_set.count()
    GetDoorsCount.short_description = 'Doors'
    def GetPagesCount(self):
        return self.doorway_set.aggregate(x=Sum('pagesCount'))['x']
    GetPagesCount.short_description = 'Pages'
    def GetDocumentRoot(self):
        '''Путь к корню сайта на сервере'''
        try:
            return self.host.rootDocumentTemplate % self.name
        except:
            return ''
    def IsFolderFree(self, folder):
        '''Свободна ли указанная папка?'''
        return self.doorway_set.filter(domainFolder=folder).count() == 0
    def save(self, *args, **kwargs):
        '''Новый домен добавляем в панель управления'''
        try:
            if self.stateSimple == 'new':
                error = AddDomainToControlPanel(self.name, self.host.controlPanelType, self.host.controlPanelUrl)
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
                                              niche=self.niche, 
                                              host=self.host, 
                                              registrator=self.registrator, 
                                              dateRegistered=self.dateRegistered, 
                                              dateExpires=self.dateExpires, 
                                              ipAddress=self.ipAddress, 
                                              nameServer1=self.nameServer1, 
                                              nameServer2=self.nameServer2, 
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
        verbose_name_plural = '3.3. Templates'
    def GetDoorsCount(self):
        return self.doorway_set.count()
    GetDoorsCount.short_description = 'Doors'
    def GetPagesCount(self):
        return self.doorway_set.aggregate(x=Sum('pagesCount'))['x']
    GetPagesCount.short_description = 'Pages'
    
class Net(BaseDoorObject, BaseDoorObjectActivatable, BaseDoorObjectTrackable):
    '''Сетка доров'''
    netLinksList = models.TextField('Links', default='', blank=True)  # ссылки сетки для линковки и спама
    class Meta:
        verbose_name = 'Net'
        verbose_name_plural = '3.4. Nets'
    def GetDoorsCount(self):
        return self.doorway_set.count()
    GetDoorsCount.short_description = 'Doors'
    def GetPagesCount(self):
        return self.doorway_set.aggregate(x=Sum('pagesCount'))['x']
    GetPagesCount.short_description = 'Pages'
    def _AddSpamLinks(self, doorway):
        '''Добавление собственных ссылок дорвея в ссылки сетки'''
        links = self.netLinksList.split('\n')
        links.extend(doorway.spamLinksList.split('\n'))
        links = MakeListUnique(links)
        self.netLinksList = '\n'.join(links)
        self.save()
    
class KeywordsSet(BaseDoorObject, BaseDoorObjectActivatable):
    '''Набор ключевых слов. Folder-based.'''
    niche = models.ForeignKey(Niche, verbose_name='Niche', null=True)
    localFolder = models.CharField('Local Folder', max_length=200, default='')
    encoding = models.CharField('Encoding', max_length=50, choices=encodings, default='utf-8')
    keywordsCount = models.IntegerField('Keywords', null=True, blank=True)
    class Meta:
        verbose_name = 'Keywords Set'
        verbose_name_plural = '3.2. Keywords Sets'
    def GetDoorsCount(self):
        return self.doorway_set.count()
    GetDoorsCount.short_description = 'Doors'
    def GetPagesCount(self):
        return self.doorway_set.aggregate(x=Sum('pagesCount'))['x']
    GetPagesCount.short_description = 'Pages'
    def GenerateKeywordsList(self, count):
        '''Сгенерировать набор ключевых слов по теме'''
        try:
            return SelectKeywords(self.localFolder, self.encoding, count)
        except Exception as error:
            EventLog('error', 'Cannot generate keywords list', self, error)

class DoorgenProfile(BaseDoorObject, BaseDoorObjectActivatable):
    '''Профиль доргена'''
    settings = models.TextField('Settings', default='')
    class Meta:
        verbose_name = 'Doorgen Profile'
        verbose_name_plural = '3.5. Doorgen Profiles'
    def GetDoorsCount(self):
        return self.doorway_set.count()
    GetDoorsCount.short_description = 'Doors'
    def GetPagesCount(self):
        return self.doorway_set.aggregate(x=Sum('pagesCount'))['x']
    GetPagesCount.short_description = 'Pages'
    
class DoorwaySchedule(BaseDoorObject, BaseDoorObjectActivatable):
    '''Менеджер генерации дорвеев'''
    net = models.ForeignKey(Net, verbose_name='Net', null=True)
    niche = models.ForeignKey(Niche, verbose_name='Niche', null=True)
    template = models.ForeignKey(Template, verbose_name='Template', null=True, blank=True)
    keywordsSet = models.ForeignKey(KeywordsSet, verbose_name='Keywords Set', null=True, blank=True)
    doorgenProfile = models.ForeignKey(DoorgenProfile, verbose_name='Drg Prof.', null=True)
    minPagesCount = models.IntegerField('Min Pgs', null=True)
    maxPagesCount = models.IntegerField('Max Pgs', null=True)
    minSpamLinksPercent = models.FloatField('Min Lnk, %', default=1)
    maxSpamLinksPercent = models.FloatField('Max Lnk, %', default=2.5)
    dateStart = models.DateField('Start Date', null=True, blank=True)
    dateEnd = models.DateField('End Date', null=True, blank=True)
    doorsPerDay = models.IntegerField('Drs/Day', null=True)
    lastRun = models.DateTimeField('Last Run Date', null=True)
    doorsThisDay = models.IntegerField('Drs ths Day', null=True, default=0)
    class Meta:
        verbose_name = 'Doorway Schedule'
        verbose_name_plural = '3.6. Doorway Schedule'
    def GetDoorsCount(self):
        return self.doorway_set.count()
    GetDoorsCount.short_description = 'Doors'
    def GetPagesCount(self):
        return self.doorway_set.aggregate(x=Sum('pagesCount'))['x']
    GetPagesCount.short_description = 'Pages'
    def _NewDateCome(self):
        '''Настали новые сутки по сравнению с lastRun?'''
        try:
            return datetime.datetime.now().strftime('%d.%m.%Y') != self.lastRun.strftime('%d.%m.%Y')
        except:
            return True
    def _GenerateDoorwaysPrivate(self, count):
        '''Генерируем дорвей'''
        if count > 0:
            for _ in range(0, count):
                p = Doorway.objects.create(net=self.net, 
                                           niche=self.niche, 
                                           template=self.template, 
                                           keywordsSet=self.keywordsSet, 
                                           doorgenProfile=self.doorgenProfile, 
                                           pagesCount=random.randint(self.minPagesCount, self.maxPagesCount), 
                                           domainFolder='', 
                                           spamLinksCount=0, 
                                           doorwaySchedule=self)
                '''Число ссылок для спама задается в процентах, 
                а в абсолютных числах должно быть не меньше трех и не больше страниц дора'''
                p.spamLinksCount = min(p.pagesCount, max(3, int(p.pagesCount * random.uniform(self.minSpamLinksPercent, self.maxSpamLinksPercent) / 100.0)))
                p.save()
        
    def GenerateDoorways(self, count = None):
        '''Определяем сколько дорвеев надо сгенерировать и генерируем'''
        try:
            if count == None:  # число дорвеев не задано, определяем сами
                if self._NewDateCome():  # если настал новый день
                    if self.doorsThisDay > 0:  # генерим оставшиеся дорвеи за вчера, если вчера был сгенерирован хотя бы один дорвей
                        self._GenerateDoorwaysPrivate(self.doorsPerDay - self.doorsThisDay)
                    self.doorsThisDay = 0  # обнуляем число сгенерированных за сегодня дорвеев
                d = datetime.datetime.now()
                count = int(round(self.doorsPerDay * (d.hour * 60.0 + d.minute) / (24 * 60))) - self.doorsThisDay
            elif self._NewDateCome():  # если число задано и настал новый день
                self.doorsThisDay = 0  # обнуляем число сгенерированных за сегодня дорвеев
            self._GenerateDoorwaysPrivate(count)  # генерим дорвеи за сегодня
            self.lastRun = datetime.datetime.now()  # обновляем статистику
            self.doorsThisDay += count
        except Exception as error:
            EventLog('error', 'Cannot generate dorways', self, error)
        self.save()
        
class Doorway(BaseDoorObject, BaseDoorObjectTrackable, BaseDoorObjectManaged):
    '''Дорвей'''
    net = models.ForeignKey(Net, verbose_name='Net', null=True)
    niche = models.ForeignKey(Niche, verbose_name='Niche', null=True)
    template = models.ForeignKey(Template, verbose_name='Template', null=True, blank=True)
    keywordsSet = models.ForeignKey(KeywordsSet, verbose_name='Kwrds Set', null=True, blank=True)
    doorgenProfile = models.ForeignKey(DoorgenProfile, verbose_name='Drg Prof.', null=True)
    pagesCount = models.IntegerField('Pgs', null=True)
    domain = models.ForeignKey(Domain, verbose_name='Domain', null=True, blank=True)
    domainFolder = models.CharField('Domain Folder', max_length=200, default='', blank=True)
    spamLinksCount = models.IntegerField('Lnks', null=True)
    doorwaySchedule = models.ForeignKey(DoorwaySchedule, verbose_name='Schedule', null=True, blank=True)
    keywordsList = models.TextField('Keywords List', default='', blank=True)
    netLinksList = models.TextField('Net Links', default='', blank=True)  # ссылки сетки для линковки этого дорвея
    spamLinksList = models.TextField('Self Links', default='', blank=True)  # ссылки дорвея для спама и линковки с сеткой
    class Meta:
        verbose_name = 'Doorway'
        verbose_name_plural = '3. Doorways - @big @managed'
    def GetTemplateType(self):
        return self.template.type
    GetTemplateType.short_description = 'Template Type'
    def GetSpamTasksCount(self):
        return self.spamtask_set.count()
    GetSpamTasksCount.short_description = 'Spam'
    def GetUrl(self):
        return '<a href="http://www.%s%s">%s</a>' % (self.domain.name, self.domainFolder, self.domain.name) 
    GetUrl.short_description = 'Link'
    GetUrl.allow_tags = True
    def GetTaskDetails(self):
        '''Подготовка данных для работы агента'''
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
                'ftpLogin': self.domain.host.ftpLogin, 
                'ftpPassword': self.domain.host.ftpPassword, 
                'ftpPort': self.domain.host.ftpPort})
    def SetTaskDetails(self, data):
        '''Обработка данных агента'''
        self.spamLinksList = DecodeListFromAgent(data['spamLinksList'][:self.spamLinksCount])
        pass
    def save(self, *args, **kwargs):
        '''Если не указаны шаблон, набор кеев или домен - берем случайные по нише'''
        if self.template == None:
            self.template = self.niche.GetRandomTemplate()
        if self.keywordsSet == None:
            self.keywordsSet = self.niche.GetRandomKeywordsSet()
        if self.domain == None:
            self.domain = self.niche.GetRandomDomain()
        '''Если нет ключевых слов, то генерируем'''
        if self.keywordsList == '':
            self.keywordsList = '\n'.join(self.keywordsSet.GenerateKeywordsList(self.pagesCount))
        '''Если нет ссылок сетки, то берем из сетки'''
        if self.netLinksList == '':
            self.netLinksList = self.net.netLinksList
        '''Если есть свои ссылки, то добавляем их в сетку'''
        if self.spamLinksList != '':
            self.net._AddSpamLinks(self)
        '''Если не указаны tracking fields, то заполняем по сети и нише (приоритет: net, niche).'''
        if self.analyticsId == '':
            self.analyticsId = self.net.analyticsId
        if self.analyticsId == '':
            self.analyticsId = self.niche.analyticsId
        self.piwikId = GetFirstObject([self.piwikId, self.net.piwikId, self.niche.piwikId])
        self.cyclikId = GetFirstObject([self.cyclikId, self.net.cyclikId, self.niche.cyclikId])
        '''Если не указана папка домена, то пытаемся занять корень. Если не получается,
        то придумываем новую папку по названию первого кея из списка'''
        if self.domainFolder == '':
            if self.domain.IsFolderFree(r'/'):
                self.domainFolder = r'/'
            else:
                self.domainFolder = r'/' + KeywordToUrl(self.keywordsList[:self.keywordsList.find('\n')])
        '''Если у домена не указана ниша, то устанавливаем ее'''
        if self.domain.niche == None:
            self.domain.niche = self.niche
            self.domain.save()
        '''Если на домене превышено максимальное количество доров, то отключаем домен'''
        if self.domain.GetDoorsCount() >= self.domain.maxDoorsCount:
            self.domain.active = False
            self.domain.save()
        super(Doorway, self).save(*args, **kwargs)
    
class XrumerBaseRaw(BaseXrumerBase, BaseDoorObjectManaged):
    '''Сырая база Хрумера. File-based.'''
    class Meta:
        verbose_name = 'Xrumer Raw Base'
        verbose_name_plural = '4.1. Xrumer Raw Bases - @managed'
    def GetXrumerBasesRCount(self):
        return self.xrumerbaser_set.count()
    def GetTaskDetails(self):
        '''Подготовка данных для работы агента'''
        pass
    def SetTaskDetails(self, data):
        '''Обработка данных агента'''
        pass
    GetXrumerBasesRCount.short_description = 'R-Bases'

class XrumerBaseR(BaseXrumerBase):
    '''База R для Хрумера. File-based.'''
    niche = models.ForeignKey(Niche, verbose_name='Niche', null=True)
    xrumerBaseRaw = models.ForeignKey(XrumerBaseRaw, verbose_name='Xrumer Base Raw', null=True)
    class Meta:
        verbose_name = 'Xrumer R Base'
        verbose_name_plural = '4.2. Xrumer R Bases'
    def GetSpamTasksCount(self):
        return self.spamtask_set.count()
    GetSpamTasksCount.short_description = 'Spam Tasks'
    
class SpamTask(BaseDoorObject, BaseDoorObjectManaged):
    '''Задание на спам'''
    niche = models.ForeignKey(Niche, verbose_name='Niche', null=True)
    doorways = models.ManyToManyField(Doorway, verbose_name='Doorways', null=True, blank=True)
    xrumerBaseR = models.ForeignKey(XrumerBaseR, verbose_name='Xrumer Base R', null=True, blank=True)
    spamText = models.TextField('Spam Text', default='', blank=True)
    spamLinksList = models.TextField('Spam Links', default='', blank=True)
    class Meta:
        verbose_name = 'Spam Task'
        verbose_name_plural = '4. Spam Tasks - @big @managed'
    def GetDoorsCount(self):
        return self.doorways.count()
    def GetTaskDetails(self):
        '''Подготовка данных для работы агента'''
        pass
    def SetTaskDetails(self, data):
        '''Обработка данных агента'''
        pass
    GetDoorsCount.short_description = 'Doors'
    
class XrumerProject(BaseDoorObject):
    '''Проект Хрумера. File-based.'''
    localFile = models.CharField('Local File', max_length=200)
    spamTask = models.OneToOneField(SpamTask, verbose_name='Spam Task', null=True, blank=True)
    xrumerBaseR = models.OneToOneField(XrumerBaseR, verbose_name='Xrumer Base R', null=True, blank=True)
    class Meta:
        verbose_name = 'Xrumer Project'
        verbose_name_plural = '4.3. Xrumer Projects'
    
class SnippetsSet(BaseDoorObject, BaseDoorObjectActivatable, BaseDoorObjectManaged):
    '''Сниппеты'''
    niche = models.ForeignKey(Niche, verbose_name='Niche', null=True)
    localFile = models.CharField('Local File', max_length=200, default='')
    keywordsCount = models.IntegerField('Keywords', null=True, default=1000)
    interval = models.IntegerField('Parsing Interval, h.', null=True, default=24)
    dateLastParsed = models.DateTimeField('Last Parsed', null=True, blank=True)
    phrasesList = models.TextField('Phrases', default='', blank=True)
    phrasesCount = models.IntegerField('Count', null=True, blank=True)
    class Meta:
        verbose_name = 'Snippets Set'
        verbose_name_plural = '4.4. Snippets Sets - @managed'
    def GetTaskDetails(self):
        '''Подготовка данных для работы агента'''
        return({'localFile': self.localFile, 
                'keywordsList': EncodeListForAgent('\n'.join(self.niche.GenerateKeywordsList(self.keywordsCount))), 
                'stopwordsList': EncodeListForAgent(self.niche.stopwordsList), 
                'language': self.niche.language})
    def SetTaskDetails(self, data):
        '''Обработка данных агента'''
        phrases = DecodeListFromAgent(data['phrasesList'])
        self.phrasesList = phrases
        self.phrasesCount = len(data['phrasesList']) 
        self.dateLastParsed = datetime.datetime.now()
