# coding=utf8
from django.db import models, transaction
from django.db.models import Sum, Count, Max, Q
from django.db.models.signals import pre_delete
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.core.mail import send_mail
from doorsadmin.common import SelectKeywords, CountKeywords, AddDomainToControlPanel, DelDomainFromControlPanel, AddSiteToPiwik, KeywordToUrl, GetFirstObject, EncodeListForAgent, DecodeListFromAgent, GenerateRandomWord, PrettyDate, GetCounter, GetPagesCounter, HtmlLinksToBBCodes, MakeListUnique, ReplaceZero, GenerateNetConfig
import datetime, random, os, re, MySQLdb, google, yahoo, nausea

eventTypes = (('trace', 'trace'), ('info', 'info'), ('warning', 'warning'), ('error', 'error'))
stateSimple = (('new', 'new'), ('ok', 'ok'), ('error', 'error'))
stateManaged = (('new', 'new'), ('inproc', 'inproc'), ('done', 'done'), ('error', 'error'))
languages = (('en', 'en'), ('ru', 'ru'))
encodings = (('cp1251', 'cp1251'), ('utf-8', 'utf-8'))
agentTypes = (('snippets', 'snippets'), ('doorgen', 'doorgen'), ('xrumer', 'xrumer'))
hostTypes = (('free', 'free'), ('shared', 'shared'), ('vps', 'vps'), ('dedicated', 'dedicated'))
hostControlPanelTypes = (('none', 'none'), ('ispconfig', 'isp config'), ('ispmanager', 'isp manager'), ('directadmin', 'direct admin'), ('cpanel', 'cpanel'))
templateTypes = (('classic', 'classic'), ('ddl', 'ddl'))
taskPriorities = (('high', 'high'), ('std', 'std'), ('zero', 'zero'))
baseCreationTypes = (('post', 'post'), ('reply', 'reply'), ('reg + post', 'reg + post'), ('reg + reply', 'reg + reply'))
spamBaseTypes = (('ZLinksList', 'ZLinksList'), ('RLinksList', 'RLinksList'))

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
            send_mail('Doors Administration', text + ' ' + objectName, 'alex@searchpro.name', ['alex@altstone.com'], fail_silently = True)

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
    elif taskType == 'XrumerBaseSpam':
        return XrumerBaseSpam
    elif taskType == 'SpamTask':
        return SpamTask
    elif taskType == 'XrumerBaseDoors':
        return XrumerBaseDoors
    elif taskType == 'XrumerBaseProfiles':
        return XrumerBaseProfiles

def NextYearDate():
    '''Сегодняшняя дата плюс год'''
    return datetime.date.today() + datetime.timedelta(365)

def NextBaseNumber():
    '''Следующий номер базы'''
    return max(0, XrumerBaseRaw.objects.all().aggregate(xx=Max('baseNumber'))['xx'], XrumerBaseSpam.objects.all().aggregate(xx=Max('baseNumber'))['xx'], XrumerBaseDoors.objects.all().aggregate(xx=Max('baseNumber'))['xx'], XrumerBaseProfiles.objects.all().aggregate(xx=Max('baseNumber'))['xx']) + 1

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
    trackers = models.ForeignKey('Trackers', verbose_name='Trackers', null=True, blank=True, on_delete=models.SET_NULL)
    tdsId = models.IntegerField('Tds', null=True, blank=True)
    piwikId = models.IntegerField('Pwk', null=True, blank=True)
    class Meta:
        abstract = True

class BaseXrumerBase(BaseDoorObject, BaseDoorObjectActivatable):
    '''База Хрумера'''
    baseNumber = models.IntegerField('#', unique=True, default=NextBaseNumber)
    linksCount = models.FloatField('Count, k.', null=True, blank=True)
    language = models.CharField('Language', max_length=50, choices=languages, blank=True)
    class Meta:
        abstract = True
    def __unicode__(self):
        return "#%d" % self.baseNumber

class BaseDoorObjectManaged(models.Model):
    priority = models.CharField('Prt.', max_length=20, choices = taskPriorities, default='std')
    agent = models.ForeignKey('Agent', verbose_name='Agent', null=True, blank=True, on_delete=models.SET_NULL)
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
    @classmethod
    def GetTasksList(self, agent):
        '''Получение списка задач для агента'''
        pass
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
    registeredAccountsCount = models.IntegerField('Ra.', null=True, blank=True)
    class Meta:
        abstract = True
    def SetTaskDetails(self, data):
        '''Обработка данных агента'''
        self.successCount = data['successCount']
        self.halfSuccessCount = data['halfSuccessCount']
        self.failsCount = data['failsCount']
        self.profilesCount = data['profilesCount']
        self.registeredAccountsCount = data['registeredAccountsCount']
        if (self.successCount < 500) or (self.successCount * 1.0 / (self.successCount + self.halfSuccessCount + self.failsCount + 1.0) < 0.3):
            EventLog('error', 'Too few successful posts (%d)' % self.successCount, self)
        super(BaseDoorObjectSpammable, self).SetTaskDetails(data)

class BaseXrumerBaseAdv(BaseXrumerBase, BaseDoorObjectSpammable):
    '''Предок баз профилей, доров на форумах и спама по топикам'''
    niche = models.ForeignKey('Niche', verbose_name='Niche', null=True)
    xrumerBaseRaw = models.ForeignKey('XrumerBaseRaw', verbose_name='Base Raw', null=True, on_delete=models.SET_NULL)
    snippetsSet = models.ForeignKey('SnippetsSet', verbose_name='Snippets', null=True, blank=True)
    nickName = models.CharField('Nick Name', max_length=200, default='', blank=True)
    realName = models.CharField('Real Name', max_length=200, default='', blank=True)
    password = models.CharField('Password', max_length=200, default='', blank=True)
    emailAddress = models.CharField('E.Address', max_length=200, default='niiokr2012@gmail.com')
    emailLogin = models.CharField('E.Login', max_length=200, default='niiokr2012@gmail.com')
    emailPassword = models.CharField('E.Password', max_length=200, default='kernel32')
    emailPopServer = models.CharField('E.Pop Server', max_length=200, default='pop.gmail.com')
    creationType = models.CharField('Creation Type', max_length=50, choices=baseCreationTypes, default='post')
    registerRun = models.BooleanField('Reg.', default=False)
    registerRunDate = models.DateTimeField('Register Date', null=True, blank=True)
    registerRunTimeout = models.IntegerField('Register Timeout, h.', default=48, null=True, blank=True)
    class Meta:
        abstract = True
    def ResetNames(self):
        '''Сбрасываем имена'''
        self.nickName = '#gennick[%s]' % GenerateRandomWord(12).upper()
        self.realName = '#gennick[%s]' % GenerateRandomWord(12).upper()
        self.password = GenerateRandomWord(12)
        self.save()
    def GetTaskDetailsCommon(self):
        '''Подготовка данных для работы агента - общая часть для задания на спам'''
        return {'niche': self.niche.description,
                'baseNumberMain': self.baseNumber,  # база, которую создаем, либо по которой спамим
                'baseNumberSource': self.xrumerBaseRaw.baseNumber,  # база, на основе которой создаем новую
                'snippetsFile': self.snippetsSet.localFile,
                'nickName': self.nickName, 
                'realName': self.realName, 
                'password': self.password, 
                'emailAddress': self.emailAddress.replace('@gmail.com', '+%s@gmail.com' % self.nickName), 
                'emailPassword': self.emailPassword, 
                'emailLogin': self.emailLogin, 
                'emailPopServer': self.emailPopServer, 
                'spamLinksList': [],
                'keywordsList': [],
                'creationType': self.creationType,
                'registerRun': self.registerRun}
    def SetTaskDetails(self, data):
        if self.registerRun:
            self.registerRunDate = datetime.datetime.now()
        if data['baseLinksCount'] != 0:
            self.linksCount = data['baseLinksCount'] / 1000.0
        super(BaseXrumerBaseAdv, self).SetTaskDetails(data)
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
        '''Если не надо предварительно регистрироваться, снимаем галочку'''
        if self.stateSimple == 'new':
            self.registerRun = self.creationType.find('reg') >= 0
        super(BaseXrumerBaseAdv, self).save(*args, **kwargs)

'''Real models'''

class Niche(BaseDoorObject, BaseDoorObjectActivatable, BaseDoorObjectTrackable):
    '''Тематика доров'''
    language = models.CharField('Lang.', max_length=50, choices=languages)
    stopwordsList = models.TextField('Stop Words', default='', blank=True)
    tdsSchemes = models.CharField('TDS Schemes', max_length=200, default='', blank=True)
    class Meta:
        verbose_name = 'Niche'
        verbose_name_plural = 'I.1 # Niches - [act]'
    def GetStopWordsCount(self):
        return len(self.stopwordsList.split('\n'))
    GetStopWordsCount.short_description = 'Stopw.'
    GetStopWordsCount.allow_tags = True
    def GetNetsCount(self):
        return GetCounter(self.net_set, {'active': True})
    GetNetsCount.short_description = 'Nets'
    GetNetsCount.allow_tags = True
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
    def GetXrumerBasesSpamCount(self):
        return GetCounter(self.xrumerbasespam_set, {'active': True, 'stateManaged': 'done'}, lambda x: x <= 0 and self.active)
    GetXrumerBasesSpamCount.short_description = 'Bas. R'
    GetXrumerBasesSpamCount.allow_tags = True
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
    def GetRandomBaseSpam(self):
        '''Получить случайную базу R для спама'''
        try:
            return XrumerBaseSpam.objects.filter(Q(active=True), (Q(niche=self) | Q(niche=None))).order_by('?')[:1].get()
        except Exception as error:
            EventLog('warning', 'Cannot find a spam base', self, error)
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
    def GetSpamLinks(self):
        '''Ссылки по этой нише, которые надо спамить'''
        return SpamLink.objects.filter(Q(spamTask=None), Q(doorway__niche=self), Q(makeSpam=True), Q(doorway__makeSpam=True), Q(doorway__domain__makeSpam=True), Q(doorway__domain__net__makeSpam=True))
    def GetSpamDomainLinks(self, domain):
        '''Ссылки по домену, которые надо спамить'''
        return SpamLink.objects.filter(Q(spamTask=None), Q(doorway__domain=domain), Q(makeSpam=True), Q(doorway__makeSpam=True), Q(doorway__domain__makeSpam=True), Q(doorway__domain__net__makeSpam=True))
    def _CreateSpamTask(self, xrumerBaseSpam, linksList):
        '''Создаем задание на спам'''
        if len(linksList) == 0:
            return
        spamTask = SpamTask.objects.create(xrumerBaseSpam=xrumerBaseSpam)
        spamTask.save()
        #print("spam task pk: %d" % spamTask.pk)
        for pk in linksList:
            spamLink = SpamLink.objects.get(pk=pk)
            spamLink.spamTask = spamTask
            spamLink.save()
            #print("- (%d) %s" % (pk, spamLink.url))
    def GenerateSpamTasksMultiple(self):
        '''Генерация заданий сразу в несколько баз'''
        try:
            '''Получаем список баз R для данной ниши'''
            xrumerBasesSpam = XrumerBaseSpam.objects.filter(Q(active=True), (Q(niche=self) | Q(niche=None))).order_by('?').all()
            xrumerBasesSpamCount = len(xrumerBasesSpam)
            '''Инициализация списков: список ссылок и список количеств оставшихся доменов'''
            linksLists = []
            domainsCounts = []
            for n in range(xrumerBasesSpamCount):
                linksLists.append([])
                xrumerBaseSpam = xrumerBasesSpam[n]
                domainsCounts.append(random.randint(xrumerBaseSpam.spamTaskDomainsMin, xrumerBaseSpam.spamTaskDomainsMax))
            '''Цикл по доменам с заданиями на спам'''
            domains = Domain.objects.filter(niche=self).order_by('?').all()
            for domain in domains:
                '''Получаем список непроспамленных ссылок домена'''
                spamLinks = self.GetSpamDomainLinks(domain).order_by('?').all()
                '''Распределяем их по базам'''
                for n in range(xrumerBasesSpamCount):
                    if len(spamLinks) == 0:
                        break
                    xrumerBaseSpam = xrumerBasesSpam[n]
                    linksCount = random.randint(xrumerBaseSpam.spamTaskDomainLinksMin, xrumerBaseSpam.spamTaskDomainLinksMax)
                    for spamLink in spamLinks[:linksCount]:
                        linksLists[n].append(spamLink.pk)
                    spamLinks = spamLinks[linksCount:]
                    domainsCounts[n] -= 1
                    '''Если задание сформировано'''
                    if domainsCounts[n] == 0:
                        self._CreateSpamTask(xrumerBaseSpam, linksLists[n])
                        linksLists[n] = []
                        domainsCounts[n] = random.randint(xrumerBaseSpam.spamTaskDomainsMin, xrumerBaseSpam.spamTaskDomainsMax)
            '''Сохраняем нераспределенные остатки'''
            #for n in range(xrumerBasesSpamCount):
            #    xrumerBaseSpam = xrumerBasesSpam[n]
            #    self._CreateSpamTask(xrumerBaseSpam, linksLists[n])
        except Exception as error:
            EventLog('error', 'Error in GenerateSpamTasksMultiple', self, error)

class BaseNet(BaseDoorObject, BaseDoorObjectActivatable, BaseDoorObjectTrackable):
    '''Базовый класс для сетки и плана сеток'''
    niche = models.ForeignKey('Niche', verbose_name='Niche', null=True)
    template = models.ForeignKey('Template', verbose_name='Template', null=True, blank=True)
    keywordsSet = models.ForeignKey('KeywordsSet', verbose_name='Kwrds Set', null=True, blank=True)
    minPagesCount = models.IntegerField('Pgs1', null=True, default=500)
    maxPagesCount = models.IntegerField('Pgs2', null=True, default=900)
    minSpamLinksPercent = models.FloatField('Min Lnk, %', default=4)
    maxSpamLinksPercent = models.FloatField('Max Lnk, %', default=5)
    minMaxSpamLinksCount = models.IntegerField('Min Max Lnk', null=True, default=10)
    maxMaxSpamLinksCount = models.IntegerField('Max Max Lnk', null=True, default=15)
    settings = models.TextField('Settings', default='#gen', blank=True)
    makeSpam = models.BooleanField('Sp.', default=True)
    domainGroup = models.CharField('Dmn.grp.', max_length=50, default='', blank=True)
    domainsPerDay = models.IntegerField('Dmn', default=0, null=True, blank=True)  # сколько доменов добавлять в день. при добавлении домена на нем сразу генерится дор
    doorsPerDay = models.IntegerField('Drs', default=0, null=True, blank=True)  # сколько дополнительных доров в папках на существующих доменах делать в день
    dateStart = models.DateField('Start Date', null=True, blank=True)
    dateEnd = models.DateField('End Date', null=True, blank=True)
    class Meta:
        abstract = True
    def GetNetSize(self):
        return len(self.settings.split(';'))
    GetNetSize.short_description = 'Net Size'
    GetNetSize.allow_tags = True

class NetPlan(BaseNet):
    '''План по созданию сеток'''
    netsCount = models.IntegerField('Plan', default=5, null=True, blank=True)
    generateNetsNow = models.IntegerField('Generate Now', default=0, blank=True)
    class Meta:
        verbose_name = 'Net Plan'
        verbose_name_plural = 'I.2 Net Plans'
    def GetNetsCount(self):
        return '%d/%d' % (self.net_set.count(), self.netsCount)
    GetNetsCount.short_description = 'Nets'
    GetNetsCount.allow_tags = True
    def GetDomainsCount(self):
        return '%d' % self.GetNetSize()
    GetDomainsCount.short_description = 'Domains'
    GetDomainsCount.allow_tags = True
    def GenerateNets(self, count = 1):
        '''Генерация сетей'''
        netsGenerated = 0
        while (self.net_set.count() < self.netsCount) and (count > 0):
            net = Net.objects.create(description='%s %.3d' % (self.description, self.net_set.count() + 1),
                                     niche=self.niche,
                                     template=self.template,
                                     keywordsSet=self.keywordsSet,
                                     minPagesCount=self.minPagesCount,
                                     maxPagesCount=self.maxPagesCount,
                                     minSpamLinksPercent=self.minSpamLinksPercent,
                                     maxSpamLinksPercent=self.maxSpamLinksPercent,
                                     minMaxSpamLinksCount=self.minMaxSpamLinksCount,
                                     maxMaxSpamLinksCount=self.maxMaxSpamLinksCount,
                                     settings=self.settings,
                                     makeSpam=self.makeSpam,
                                     domainGroup=self.domainGroup,
                                     domainsPerDay=self.domainsPerDay,
                                     doorsPerDay=self.doorsPerDay,
                                     dateStart=datetime.date.today(),
                                     netPlan=self)
            net.save()
            count -= 1
            netsGenerated += 1
        return netsGenerated
    def save(self, *args, **kwargs):
        '''Немедленная генерация сетей'''
        if self.generateNetsNow > 0:
            n = self.generateNetsNow
            self.generateNetsNow = 0
            self.GenerateNets(n)
        super(NetPlan, self).save(*args, **kwargs)

class Net(BaseNet):
    '''Сетка доров'''
    addDomainsNow = models.IntegerField('Add domains now', default=0, blank=True)
    generateDoorsNow = models.IntegerField('Generate doors Now', default=0, blank=True)
    netPlan = models.ForeignKey('NetPlan', verbose_name='Net Plan', null=True, blank=True, on_delete=models.SET_NULL)
    class Meta:
        verbose_name = 'Net'
        verbose_name_plural = 'I.3.a Nets - [act]'
    def GetDoorsCount(self):
        return ReplaceZero(self.domain_set.annotate(x=Count('doorway')).aggregate(xx=Sum('x'))['xx'])
    GetDoorsCount.short_description = 'Doors'
    GetDoorsCount.allow_tags = True
    def GetPagesCount(self):
        return ReplaceZero(self.domain_set.annotate(x=Sum('doorway__pagesCount')).aggregate(xx=Sum('x'))['xx'])
    GetPagesCount.short_description = 'Pages'
    GetPagesCount.allow_tags = True
    def GetDomainsCount(self):
        return '%d/%d' % (self.domain_set.count(), self.GetNetSize())
    GetDomainsCount.short_description = 'Domains'
    GetDomainsCount.allow_tags = True
    def GetIndexCount(self):
        return ReplaceZero(self.domain_set.aggregate(x = Sum('indexCount'))['x'])
    GetIndexCount.short_description = 'Index'
    GetIndexCount.allow_tags = True
    def GetBackLinksCount(self):
        return ReplaceZero(self.domain_set.aggregate(x = Sum('backLinksCount'))['x'])
    GetBackLinksCount.short_description = 'YBL'
    GetBackLinksCount.allow_tags = True
    def GetNextDomain(self):
        '''Получить следующий свободный домен'''
        try:
            for obj in self.domain_set.filter(active=True).order_by('pk').all():
                if obj.IsRootFree():
                    return obj
            return Domain.objects.filter(Q(active=True), Q(net=self)).order_by('?')[:1].get()
        except Exception as error:
            EventLog('error', 'Cannot find a domain', self, error)
    def AddDomains(self, count = None, domainsLimit = 9999, linksLimit = 9999):
        '''Добавление доменов в сетку. Аргументы: 
        count - сколько доменов присоединять, 
        domainsLimit - лимит по доменам, 
        linksLimit - максимальное количество ссылок для спама на сгенеренных дорах. 
        Возвращает обновленные лимиты.'''
        if self.settings == '':
            return domainsLimit, linksLimit
        if count == None:
            count = self.domainsPerDay
        netChain = self.settings.split(';')
        netDomains = self.domain_set.order_by('pk')
        '''Цикл по активным и непривязанным к сеткам доменам, у которых ниша и группа пустые или совпадают с параметрами сетки'''
        for domain in Domain.objects.filter(Q(net=None), (Q(niche=self.niche) | Q(niche=None)), (Q(group=self.domainGroup) | Q(group='')), Q(active=True)).order_by('-group', 'pk').all():  # сначала берем домены из группы, затем без группы
            if (count <= 0) or (domainsLimit <= 0) or (linksLimit <= 0) or (netDomains.count() >= len(netChain)):
                break
            try:
                domain.linkedDomains.clear()
                '''Цикл по доменам, к которым надо привязать новый домен'''
                for n in netChain[netDomains.count()].split('-')[1:]:
                    domain.linkedDomains.add(netDomains[int(n) - 1])
                domain.net = self
                domain.niche = self.niche
                domain.save()
                count -= 1
                domainsLimit -= 1
                '''Генерируем дорвей'''
                linksLimit = self.GenerateDoorways(1, domain, linksLimit)
                '''Код дублируется для возможности проводить вязку сетей в одном цикле'''
                netDomains = self.domain_set.order_by('pk')
            except Exception as error:
                EventLog('error', 'Error in AddDomains', self, error)
        '''Если сеть полностью построена'''
        self.domainsPerDay = max(0, min(self.domainsPerDay, len(netChain) - netDomains.count()))
        self.save()
        return domainsLimit, linksLimit
    def GenerateDoorways(self, count = None, domain = None, linksLimit = 9999):
        '''Генерация дорвеев. Аргументы: count - сколько дорвеев генерировать, 
        domain - на каком домене генерировать, linksLimit - максимальное количество 
        ссылок для спама на сгенеренных дорах. Возвращает обновленный лимит.'''
        if count == None:
            count = self.doorsPerDay
        if domain == None:
            domain = self.GetNextDomain()
            if domain == None:
                return linksLimit
        for _ in range(0, count):
            if (linksLimit <= 0):
                break
            try:
                p = Doorway.objects.create(niche=self.niche, 
                                           template=self.template, 
                                           keywordsSet=self.keywordsSet, 
                                           pagesCount = random.randint(self.minPagesCount, self.maxPagesCount), 
                                           domain=domain, 
                                           domainFolder='')
                p.spamLinksCount = int(p.pagesCount * random.uniform(self.minSpamLinksPercent, self.maxSpamLinksPercent) / 100.0)  # число ссылок для спама: берем в процентах от количества страниц дора, 
                p.spamLinksCount = max(p.spamLinksCount, 3)  # минимум три,
                #p.spamLinksCount = min(p.spamLinksCount, random.randint(self.minMaxSpamLinksCount, self.maxMaxSpamLinksCount))  # максимум из настроек сети,
                p.spamLinksCount = min(p.spamLinksCount, p.pagesCount)  # максимум число страниц дора.
                p.save()
                linksLimit -= (p.spamLinksCount + 1)  # + карта сайта
            except Exception as error:
                EventLog('error', 'Error in GenerateDoorways', self, error)
        return linksLimit
    def save(self, *args, **kwargs):
        '''Создаем сайт на Piwik'''
        try:
            if self.stateSimple == 'new' and self.piwikId == None:
                self.piwikId = int(AddSiteToPiwik(self.description))
        except Exception as error:
            EventLog('error', 'Cannot add site to Piwik', None, error)
        '''Автогенерация сетки'''
        try:
            if self.stateSimple == 'new' and self.settings == '#gen':
                self.settings, _, _, _ = GenerateNetConfig(2, 4, 2, 4, 10, 25, False)
        except Exception as error:
            EventLog('error', 'Cannot generate net params', None, error)
        '''Генерируем всю сеть целиком'''
        if self.stateSimple == 'new' and self.domainsPerDay == -1:
            self.domainsPerDay = self.GetNetSize()
        '''Немендленное добавление доменов в сеть'''
        if self.addDomainsNow > 0:
            n = self.addDomainsNow
            self.addDomainsNow = 0
            self.AddDomains(n)
        '''Немедленная генерация доров в сетке'''
        if self.generateDoorsNow > 0:
            n = self.generateDoorsNow
            self.generateDoorsNow = 0
            self.GenerateDoorways(n)
        super(Net, self).save(*args, **kwargs)

class NetDescription(Net):
    '''Класс для отображения еще одной строки в админке'''
    class Meta:
        verbose_name = 'Net Description'
        verbose_name_plural = 'I.3.b Net Descriptions'
        proxy = True

class KeywordsSet(BaseDoorObject, BaseDoorObjectActivatable):
    '''Набор ключевых слов'''
    niche = models.ForeignKey('Niche', verbose_name='Niche', null=True)
    localFolder = models.CharField('Local Folder', max_length=200, default='')
    encoding = models.CharField('Encoding', max_length=50, choices=encodings, default='cp1251')
    keywordsCount = models.FloatField('Keys Count, k.', null=True, blank=True)
    class Meta:
        verbose_name = 'Keywords Set'
        verbose_name_plural = 'I.4 Keywords Sets - [act]'
    def GetLocalFolder(self):
        s = self.localFolder
        s = s.replace('/home/admin/public_html/searchpro.name/web/doorscenter/doorsadmin/keywords/', '/')
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

class Template(BaseDoorObject, BaseDoorObjectActivatable):
    '''Шаблон дора'''
    type = models.CharField('Type', max_length=50, choices=templateTypes, default='classic')
    niche = models.ForeignKey('Niche', verbose_name='Niche', null=True, blank=True)
    agent = models.ForeignKey('Agent', verbose_name='Agent', null=True, blank=True)
    localFolder = models.CharField('Local Folder', max_length=200, default='')
    class Meta:
        verbose_name = 'Template'
        verbose_name_plural = 'I.5 Templates - [act]'
    def __unicode__(self):
        return self.localFolder
    def GetDoorsCount(self):
        return GetCounter(self.doorway_set, {'stateManaged': 'done'})
    GetDoorsCount.short_description = 'Doors'
    GetDoorsCount.allow_tags = True
    def GetPagesCount(self):
        return GetPagesCounter(self.doorway_set)
    GetPagesCount.short_description = 'Pages'
    GetPagesCount.allow_tags = True

class SnippetsSet(BaseDoorObject, BaseDoorObjectActivatable, BaseDoorObjectManaged):
    '''Сниппеты'''
    niche = models.ForeignKey('Niche', verbose_name='Niche', null=True)
    localFile = models.CharField('Local File', max_length=200, default='')
    keywordsCount = models.IntegerField('Keywords', null=True, default=200)
    interval = models.IntegerField('Interval, h.', null=True, default=100)
    dateLastParsed = models.DateTimeField('Last Parsed', null=True, blank=True)
    phrasesCount = models.IntegerField('Count', null=True, blank=True)
    class Meta:
        verbose_name = 'Snippets Set'
        verbose_name_plural = 'I.6 Snippets Sets - [act, managed]'
    def GetDateLastParsedAgo(self):
        return PrettyDate(self.dateLastParsed)
    GetDateLastParsedAgo.short_description = 'Last Parsed'
    @classmethod
    def GetTasksList(self, agent):
        '''Получение списка задач для агента'''
        return SnippetsSet.objects.filter(Q(stateManaged='new'), Q(active=True)).order_by('priority', 'pk')
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
            EventLog('error', 'Too few snippets found: %d' % self.phrasesCount, self)
        super(SnippetsSet, self).SetTaskDetails(data)

class Domain(BaseDoorObject, BaseDoorObjectActivatable):
    '''Домен'''
    name = models.CharField('Domain Name', max_length=200, unique=True)
    net = models.ForeignKey('Net', verbose_name='Net', null=True, blank=True, on_delete=models.SET_NULL)
    niche = models.ForeignKey('Niche', verbose_name='Niche', null=True, blank=True)
    host = models.ForeignKey('Host', verbose_name='Host', null=True)
    registrator = models.CharField('Registrator', max_length=200, default='', blank=True)
    dateRegistered = models.DateField('Registered', default=datetime.date.today, null=True, blank=True)
    dateExpires = models.DateField('Expires', default=NextYearDate, null=True, blank=True)
    ipAddress = models.ForeignKey('IPAddress', verbose_name='IP Address', null=True)
    nameServer1 = models.CharField('NS 1', max_length=200, default='', blank=True)
    nameServer2 = models.CharField('NS 2', max_length=200, default='', blank=True)
    useOwnDNS = models.BooleanField('Use own DNS', default=False, blank=True)
    linkedDomains = models.ManyToManyField('self', verbose_name='Linked Domains', symmetrical=False, null=True, blank=True)
    bulkAddDomains = models.TextField('More Domains', default='', blank=True)
    maxDoorsCount = models.IntegerField('Max Doors', default=10, blank=True)
    makeSpam = models.BooleanField('Sp.', default=True)
    group = models.CharField('Group', max_length=50, default='', blank=True)
    indexCount = models.IntegerField('Index', null=True, blank=True)
    indexCountDate = models.DateField('Index Date', null=True, blank=True)
    backLinksCount = models.IntegerField('YBL', null=True, blank=True)
    backLinksCountDate = models.DateField('YBL Date', null=True, blank=True)
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
    def GetNetLinksList(self, doorwayToExclude):
        '''Ссылки для перелинковки'''
        linksList = []
        '''Ссылки с других доров этого домена'''
        for doorway in self.doorway_set.filter(stateManaged='done').order_by('pk').all():
            if doorway != doorwayToExclude:
                linksList.extend(doorway.GetSpamLinksList().split('\n'))
        '''Корень не линкуем с другими доменами'''
        if doorwayToExclude.domainFolder not in ['', r'/']:
            '''Ссылки с других доменов'''
            for domain in self.linkedDomains.filter(pk__lt=self.pk).order_by('pk').all():
                for doorway in domain.doorway_set.filter(stateManaged='done').order_by('pk').all():
                    linksList.extend(doorway.GetSpamLinksList().split('\n'))
        return '\n'.join(MakeListUnique(linksList))
    def GetIndexCount(self):
        '''Ссылка для проверки индекса по гуглу'''
        if self.indexCount:
            return '<a href="%s">%d</a>' % (google.GetIndexLink(self.name), self.indexCount)
        else:
            return '<a href="%s">-</a>' % (google.GetIndexLink(self.name))
    GetIndexCount.short_description = 'Index'
    GetIndexCount.allow_tags = True
    def UpdateIndexCount(self):
        '''Проверяем индекс в гугле'''
        self.indexCount = google.GetIndex(self.name)
        self.indexCountDate = datetime.datetime.now()
        self.save()
    def GetBackLinksCount(self):
        '''Ссылка для проверки YBL'''
        if self.backLinksCount:
            return '<a href="%s">%d</a>' % (yahoo.GetBackLinksLink(self.name), self.backLinksCount)
        else:
            return '<a href="%s">-</a>' % (yahoo.GetBackLinksLink(self.name))
    GetBackLinksCount.short_description = 'YBL'
    GetBackLinksCount.allow_tags = True
    def UpdateBackLinksCount(self):
        '''Проверяем YBL'''
        self.backLinksCount = yahoo.GetBackLinks(self.name)
        self.backLinksCountDate = datetime.datetime.now()
        self.save()
    def CheckOwnership(self):
        '''Проверка на то, что домен не отобрали'''
        dnsRecord = os.popen('dig %s +short' % self.name).read().replace('\n', ' ').strip()
        if self.ipAddress.address == dnsRecord:
            return True
        self.active = False
        self.stateSimple = 'error'
        self.lastError = 'DNS record is %s' % dnsRecord
        self.save()
        return False
    def Reset(self):
        '''Сбрасываем параметры домена'''
        self.niche = None
        self.net = None
        self.active = True
        self.save()
    def save(self, *args, **kwargs):
        '''Если в имени домена стоит #, то его не добавляем, а берем имена из bulkAddDomains'''
        try:
            '''Новый домен добавляем в панель управления'''
            if (self.name != '#') and (self.stateSimple == 'new'):
                error = AddDomainToControlPanel(self.name, self.ipAddress.address, self.useOwnDNS, self.host.controlPanelType, self.host.controlPanelUrl, self.host.controlPanelServerId)
                if error != '':
                    self.lastError = error
                    self.stateSimple = 'error'
                    self.save()
        except Exception as error:
            EventLog('error', 'Cannot add domain to control panel', self, error)
        '''Групповое добавление доменов с теми же параметрами'''
        if (self.name == '#') and (self.bulkAddDomains != ''):
            for domainName in self.bulkAddDomains.lower().splitlines():
                if domainName != '':
                    try:
                        domain = Domain.objects.create(name=domainName, 
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
                                              group=self.group)
                        domain.save()
                    except Exception as error:
                        EventLog('error', 'Cannot add additional domain "%s"' % domainName, self, error)
        '''Всегда очищаем поле группового добавления доменов'''
        self.bulkAddDomains = ''
        super(Domain, self).save(*args, **kwargs)

def DomainOnDelete(sender, **kwargs):
    '''Событие на удаление домена'''
    domain = kwargs['instance']
    try:
        if domain.name != '#':
            error = DelDomainFromControlPanel(domain.name, domain.host.controlPanelType, domain.host.controlPanelUrl)
            if error != '':
                EventLog('error', 'Cannot delete domain from control panel', domain, error)
    except Exception as error:
        EventLog('error', 'Cannot delete domain from control panel', domain, error)
pre_delete.connect(DomainOnDelete, sender=Domain, weak=False)

class Doorway(BaseDoorObject, BaseDoorObjectTrackable, BaseDoorObjectManaged):
    '''Дорвей'''
    niche = models.ForeignKey('Niche', verbose_name='Niche', null=True)
    template = models.ForeignKey('Template', verbose_name='Template', null=True, blank=True)
    keywordsSet = models.ForeignKey('KeywordsSet', verbose_name='Kwrds Set', null=True, blank=True)
    pagesCount = models.IntegerField('Pgs', null=True)
    domain = models.ForeignKey('Domain', verbose_name='Domain', null=True, blank=True)
    domainFolder = models.CharField('Domain Folder', max_length=200, default='', blank=True)
    spamLinksCount = models.IntegerField('Lnks', null=True)
    keywordsList = models.TextField('Keywords List', default='', blank=True)
    netLinksList = models.TextField('Net Links', default='', blank=True)  # ссылки сетки для линковки этого дорвея
    makeSpam = models.BooleanField('Sp.', default=True)
    class Meta:
        verbose_name = 'Doorway'
        verbose_name_plural = 'II.2 Doorways - [large, managed]'
    def __unicode__(self):
        return 'http://%s%s' % (self.domain.name, self.domainFolder)
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
        return '%s/%d' % (s1, self.spamLinksCount + 1)  # дополнительная ссылка - карта сайта
    GetSpamLinksCount.short_description = 'Lnks'
    GetSpamLinksCount.allow_tags = True
    def GetSpamLinksList(self):
        '''Получаем список ссылок для спама'''
        s = ''
        for spamLink in SpamLink.objects.filter(doorway=self):
            s += '<a href="%s">%s</a>\n' % (spamLink.url, spamLink.anchor)
        return s
    @classmethod
    def GetTasksList(self, agent):
        '''Получение списка задач для агента'''
        return Doorway.objects.filter(Q(stateManaged='new'), (Q(agent=agent) | Q(agent=None))).order_by('priority', 'pk')
    def GetTaskDetails(self):
        '''Подготовка данных для работы агента'''
        if self.netLinksList == '':
            self.netLinksList = self.domain.GetNetLinksList(self)
        keywordsListAdd = '\n'.join(self.keywordsSet.GenerateKeywordsList(min(self.pagesCount * 5, 5000)))
        return({
                'keywordsList': EncodeListForAgent(self.keywordsList), 
                'keywordsListAdd': EncodeListForAgent(keywordsListAdd), 
                'templateFolder': self.template.localFolder, 
                'doorgenSettings': EncodeListForAgent(''),  # deprecated 
                'domain': self.domain.name, 
                'domainFolder': self.domainFolder, 
                'netLinksList': EncodeListForAgent(self.netLinksList),
                #'tdsUrl': self.trackers.tdsUrl,
                'tdsId': self.tdsId,
                #'piwikUrl': self.trackers.piwikUrl,
                'piwikId': self.piwikId,
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
        '''Проверяем дор на тошноту'''
        isGood, details = nausea.Analyze('http://%s%s' % (self.domain.name, self.domainFolder), True)
        if not isGood:
            EventLog('warning', details)
            #send_mail('Doors Administration', details, 'alex@searchpro.name', ['alex@altstone.com'], fail_silently = True)
        super(Doorway, self).SetTaskDetails(data)
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
            self.netLinksList = self.domain.GetNetLinksList(self)
        '''Если не указаны tracking fields, то заполняем по сети и нише (приоритет: net, niche).'''
        try:
            self.trackers = GetFirstObject([self.trackers, self.domain.net.trackers, self.niche.trackers])
        except Exception:
            pass
        try:
            self.tdsId = GetFirstObject([self.tdsId, self.domain.net.tdsId, self.niche.tdsId])
        except Exception:
            pass
        try:
            self.piwikId = GetFirstObject([self.piwikId, self.domain.net.piwikId, self.niche.piwikId])
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
        '''Если не указан желаемый агент, берем из шаблона'''
        if (self.agent == None) and (self.template != None):
            self.agent = self.template.agent
        super(Doorway, self).save(*args, **kwargs)

class SpamLink(models.Model):
    '''Ссылки для спама'''
    url = models.CharField('URL', max_length=1000, default='')
    anchor = models.CharField('Anchor', max_length=1000, default='')
    doorway = models.ForeignKey('Doorway', verbose_name='Doorway')
    spamTask = models.ForeignKey('SpamTask', verbose_name='Spam Task', null=True, blank=True, on_delete=models.SET_NULL)
    makeSpam = models.BooleanField('Sp.', default=True)
    class Meta:
        verbose_name = 'Spam Link'
        verbose_name_plural = 'II.3 Spam Links - [large]'
    def __unicode__(self):
        return self.url
    def IsAssigned(self):
        return self.spamTask != None
    IsAssigned.short_description = 'Ass.'
    IsAssigned.allow_tags = True
    def GetSpamTaskState(self):
        '''Состояние задания на спам'''
        if (self.spamTask):
            return self.spamTask.stateManaged
        else:
            return '-'
    GetSpamTaskState.short_description = 'Spam State'
    GetSpamTaskState.allow_tags = True

class XrumerBaseSpam(BaseXrumerBaseAdv):
    '''База R для спама по топикам'''
    baseType = models.CharField('Base Type', max_length=50, choices=spamBaseTypes, default='RLinksList')
    spamTaskDomainsMin = models.IntegerField('Spam Task Domains Min', default = 3)
    spamTaskDomainsMax = models.IntegerField('Spam Task Domains Max', default = 5)
    spamTaskDomainLinksMin = models.IntegerField('Spam Task Domain Links Min', default = 3)
    spamTaskDomainLinksMax = models.IntegerField('Spam Task Domain Links Max', default = 5)
    class Meta:
        verbose_name = 'Xrumer Base Spam'
        verbose_name_plural = 'II.4 Xrumer Bases Spam - [act, managed]'
    def GetSpamTasksCount(self):
        return GetCounter(self.spamtask_set, {'stateManaged': 'done'})
    GetSpamTasksCount.short_description = 'Spam'
    GetSpamTasksCount.allow_tags = True
    def GetSpamTaskDomainLinksCount(self):
        return random.randint(self.spamTaskDomainLinksMin, self.spamTaskDomainLinksMax)
    @classmethod
    def GetTasksList(self, agent):
        '''Получение списка задач для агента'''
        return XrumerBaseSpam.objects.filter(Q(stateManaged='new'), Q(active=True)).order_by('priority', 'pk')
    def GetTaskDetails(self):
        '''Подготовка данных для работы агента'''
        result = self.GetTaskDetailsCommon()
        result['snippetsFile'] = self.niche.GetRandomSnippetsSet().localFile
        result['keywordsList'] = self.niche.GenerateKeywordsList(5000)
        result['baseType'] = self.baseType
        return result
    def SetTaskDetails(self, data):
        '''Обработка данных агента'''
        super(XrumerBaseSpam, self).SetTaskDetails(data)

class SpamTask(BaseDoorObject, BaseDoorObjectSpammable):
    '''Задание на спам'''
    xrumerBaseSpam = models.ForeignKey('XrumerBaseSpam', verbose_name='Base Spam', null=True)
    class Meta:
        verbose_name = 'Spam Task'
        verbose_name_plural = 'II.5 Spam Tasks - [large, managed]'
    def GetSpamLinksList(self):
        '''Получаем список ссылок для спама'''
        s = ''
        for spamLink in SpamLink.objects.filter(spamTask=self):
            s += '<a href="%s">%s</a>\n' % (spamLink.url, spamLink.anchor)
        return s
    @classmethod
    def GetTasksList(self, agent):
        '''Получение списка задач для агента'''
        return SpamTask.objects.filter(Q(stateManaged='new')).order_by('priority', 'pk')
    def GetTaskDetails(self):
        '''Подготовка данных для работы агента'''
        result = self.xrumerBaseSpam.GetTaskDetailsCommon()
        result['snippetsFile'] = self.xrumerBaseSpam.niche.GetRandomSnippetsSet().localFile
        result['keywordsList'] = self.xrumerBaseSpam.niche.GenerateKeywordsList(5000)
        result['baseType'] = self.xrumerBaseSpam.baseType
        result['spamLinksList'] = HtmlLinksToBBCodes(EncodeListForAgent(self.GetSpamLinksList()))
        return result
    def SetTaskDetails(self, data):
        '''Обработка данных агента'''
        if data['baseLinksCount'] != 0:
            self.xrumerBaseSpam.linksCount = data['baseLinksCount'] / 1000.0
            self.xrumerBaseSpam.save()
        super(SpamTask, self).SetTaskDetails(data)

class XrumerBaseDoors(BaseXrumerBaseAdv):
    '''База R для доров на форумах'''
    body = models.TextField('Body', default='', blank=True)
    runCount = models.IntegerField('Run Count', default=100, null=True, blank=True)
    class Meta:
        verbose_name = 'Xrumer Base Doors'
        verbose_name_plural = 'II.6 Xrumer Bases Doors - [act, managed]'
    @classmethod
    def GetTasksList(self, agent):
        '''Получение списка задач для агента'''
        return XrumerBaseDoors.objects.filter(Q(stateManaged='new'), Q(active=True)).order_by('priority', '?')
    def GetTaskDetails(self):
        '''Подготовка данных для работы агента'''
        result = self.GetTaskDetailsCommon()
        result['body'] = self.body
        result['keywordsList'] = self.niche.GenerateKeywordsList(5000)
        return result
    def SetTaskDetails(self, data):
        '''Обработка данных агента'''
        if (self.runCount > 0) and (data['state'] == 'done'):
            self.runCount -= 1
            self.save()
            data['state'] = 'new'
        super(XrumerBaseDoors, self).SetTaskDetails(data)

class XrumerBaseProfiles(BaseXrumerBaseAdv):
    '''База профилей'''
    homePage = models.CharField('Home page', max_length=200, default='', blank=True)
    signature = models.CharField('Signature', max_length=200, default='', blank=True)
    class Meta:
        verbose_name = 'Xrumer Base Profiles'
        verbose_name_plural = 'II.7 Xrumer Bases Profiles - [act, managed]'
    @classmethod
    def GetTasksList(self, agent):
        '''Получение списка задач для агента'''
        return XrumerBaseProfiles.objects.filter(Q(stateManaged='new'), Q(active=True)).order_by('priority', 'pk')
    def GetTaskDetails(self):
        '''Подготовка данных для работы агента'''
        result = self.GetTaskDetailsCommon()
        result['homePage'] = self.homePage
        result['signature'] = self.signature
        return result
    def SetTaskDetails(self, data):
        '''Обработка данных агента'''
        super(XrumerBaseProfiles, self).SetTaskDetails(data)
    def save(self, *args, **kwargs):
        if self.stateSimple == 'new':
            self.creationType = 'reg + post'
        if self.stateManaged == 'new' and self.registerRun == False and self.homePage == '':
            self.stateManaged = 'done'
            self.registerRun = True
        super(XrumerBaseProfiles, self).save(*args, **kwargs)

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
    host = models.ForeignKey('Host', verbose_name='Host', null=True, blank=True)
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

class XrumerBaseRaw(BaseXrumerBase):
    '''Сырая база Хрумера'''
    class Meta:
        verbose_name = 'Xrumer Base Raw'
        verbose_name_plural = 'III.3 Xrumer Bases Raw - [act]'
    def GetXrumerBasesSpamCount(self):
        return GetCounter(self.xrumerbasespam_set, {'active': True, 'stateManaged': 'done'})
    GetXrumerBasesSpamCount.short_description = 'Bases Spam'
    GetXrumerBasesSpamCount.allow_tags = True

class Trackers(BaseDoorObject):
    '''Связка TDS+Piwik'''
    tdsUrl = models.CharField('TDS URL', max_length=50, default='')
    piwikUrl = models.CharField('Piwik URL', max_length=50, default='')
    class Meta:
        verbose_name = 'Trackers'
        verbose_name_plural = 'III.4 Trackers'
    def __unicode__(self):
        return '%s - %s' % (self.tdsUrl, self.piwikUrl)

class Agent(BaseDoorObject, BaseDoorObjectActivatable):
    type = models.CharField('Agent Type', max_length=50, choices = agentTypes)
    currentTask = models.CharField('Current Task', max_length=200, default='', blank=True)
    dateLastPing = models.DateTimeField('Last Ping', null=True, blank=True)
    interval = models.IntegerField('Warning, h.', null=True, default=3)
    params = models.TextField('Parameters', default='', blank=True)
    class Meta:
        verbose_name = 'Agent'
        verbose_name_plural = 'IV.1 # Agents - [act]'
    def GetQueues(self):
        '''Очереди каких объектов обрабатывает агент?'''
        if self.type == 'snippets':
            return [SnippetsSet]
        elif self.type == 'doorgen':
            return [Doorway]
        elif self.type == 'xrumer':
            return [XrumerBaseProfiles, XrumerBaseSpam, SpamTask, XrumerBaseDoors]
    def AppendParams(self, data):
        '''Добавляем параметры агента в задание'''
        for param in self.params.split('\n'):
            name, _, value = param.strip().partition('=')
            if name != '':
                data[name] = value
    def OnUpdate(self):
        '''Событие апдейта задачи'''
        try:
            if self.type == 'doorgen':
                '''Генерируем задания для спама'''  
                if Doorway.objects.filter(stateManaged='new').count() == 0:
                    # def GenerateSpamTasks():
                    for niche in Niche.objects.filter(active=True).order_by('pk').all():
                        niche.GenerateSpamTasksMultiple()
        except Exception as error:
            EventLog('error', 'Error in "OnUpdate"', self, error)
    def GetDateLastPingAgo(self):
        '''Время последнего пинга в стиле "... ago"'''
        return PrettyDate(self.dateLastPing)
    GetDateLastPingAgo.short_description = 'Last Ping'
    GetDateLastPingAgo.allow_tags = True
    def GetTasksState(self):
        '''Состояние очередей агента'''
        countUndone = 0
        countDone = 0
        countError = 0
        for queue in self.GetQueues():
            countUndone += queue.GetTasksList(self).count()
            countDone += queue.objects.filter(stateManaged='done').count()
            countError += queue.objects.filter(stateManaged='error').count()
        return '%d - %d - %d' % (countUndone, countDone, countError)
    GetTasksState.short_description = 'Tasks'
    GetTasksState.allow_tags = True

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

class Report(models.Model):
    '''Отчеты'''
    description = models.CharField('Description', max_length=200, default='', blank=True)
    host = models.CharField('Host', max_length=50, default='localhost')
    user = models.CharField('User', max_length=50, default='admin')
    password = models.CharField('Password', max_length=50, default='')
    database = models.CharField('Database', max_length=50, default='')
    sql = models.TextField('SQL', default='')
    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'IV.3 Reports'
    def __unicode__(self):
        return self.description
    def GetReport(self):
        '''Результат запроса'''
        try:
            db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.database)
            try:
                cursor = db.cursor()
                try:
                    cursor.execute(self.sql)
                    results = cursor.fetchall()
                except Exception as error:
                    results = error
                cursor.close()
            except Exception as error:
                results = error
            db.close()
        except Exception as error:
            results = error
        return str(results)
    GetReport.short_description = 'Report'
    GetReport.allow_tags = True
