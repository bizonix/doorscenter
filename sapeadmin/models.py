# coding=utf8
from django.db.models import Count, Sum, Q
from django.db import models
import random, codecs, ftplib, glob, os, shutil, urllib, re, datetime, yandex

siteStates = (('new', 'new'), ('generated', 'generated'), ('uploaded', 'uploaded'), ('spammed', 'spammed'), 
              ('spam-indexed', 'spam-indexed'), ('bot-visited', 'bot-visited'), ('site-indexed', 'site-indexed'), 
              ('sape-added', 'sape-added'), ('sape-approved', 'sape-approved'), 
              ('sape-price1', 'sape-price1'), ('sape-price2', 'sape-price2'), ('sape-price3', 'sape-price3'), 
              ('sape-banned', 'sape-banned'))
spamStates = (('new', 'new'), ('inproc', 'inproc'), ('done', 'done'), ('error', 'error'))

vpbblUrl = 'http://test.home/vpbbl'
vpbblLocal = '/home/sasch/public_html/test.home/vpbbl'
if not os.path.exists(vpbblLocal):
    vpbblLocal = '/home/admin/searchpro.name/vpbbl'
    vpbblUrl = 'http://searchpro.name/vpbbl'

'''Functions'''

def GetCounter(objects, filterCondition, warningCondition = None):
    '''Возвращает общее число объектов и число, удовлетворяющее заданному условию'''
    n1 = objects.filter(**filterCondition).count()
    if n1 != 0:
        s1 = '%d' % n1
    else: 
        s1 = '-'
    n2 = objects.count()
    if n2 != 0:
        s2 = '%d' % n2
    else: 
        s2 = '-'
    if warningCondition and warningCondition(n1):
        return '<font color="red">%s/%s</font>' % (s1, s2)
    else:
        return '%s/%s' % (s1, s2)

def ReplaceZero(s):
    '''Заменяем None на тире'''
    if s == None or s == 0 or s == 'None' or s == '0':
        return '-'
    else:
        return s

'''Abstract models'''

class BaseSapeObject(models.Model):
    '''Общие атрибуты всех объектов'''
    remarks = models.TextField('Remarks', default='', blank=True)
    dateAdded = models.DateTimeField('Date Added', auto_now_add = True, null=True, blank=True)
    dateChanged = models.DateTimeField('Date Changed', auto_now_add = True, auto_now = True, null=True, blank=True)
    active = models.BooleanField('Act.', default=True)
    class Meta:
        abstract = True

'''Real models'''

class Niche(BaseSapeObject):
    '''Ниша'''
    name = models.CharField('Name', max_length=50, default='')
    priority = models.IntegerField('Priority', default=10, blank=True)
    class Meta:
        verbose_name = 'Niche'
        verbose_name_plural = 'I.1 # Niches'
    def __unicode__(self):
        return self.name
    def GetDonorsCount(self):
        return GetCounter(self.donor_set, {'active': True})
    GetDonorsCount.short_description = 'Donors'
    GetDonorsCount.allow_tags = True
    def GetArticlesCount(self):
        return ReplaceZero(self.donor_set.annotate(x=Count('article')).aggregate(xx=Sum('x'))['xx'])
    GetArticlesCount.short_description = 'Articles'
    GetArticlesCount.allow_tags = True
    def GetSitesCount(self):
        return GetCounter(self.site_set, {'active': True})
    GetSitesCount.short_description = 'Sites'
    GetSitesCount.allow_tags = True

class Donor(BaseSapeObject):
    '''Донор статей'''
    niche = models.ForeignKey('Niche', verbose_name='Niche', null=True)
    url = models.URLField('Url', default='', unique=True)
    class Meta:
        verbose_name = 'Donor'
        verbose_name_plural = 'I.2 Donors'
    def __unicode__(self):
        return '#%d' % self.pk
    def GetUrl(self):
        return '<a href="%s" target="_blank">%s</a>' % (self.url, self.url)
    GetUrl.short_description = 'Url'
    GetUrl.allow_tags = True
    def GetArticlesCount(self):
        return GetCounter(self.article_set, {'active': True})
    GetArticlesCount.short_description = 'Articles'
    GetArticlesCount.allow_tags = True

class Article(BaseSapeObject):
    '''Статья'''
    donor = models.ForeignKey('Donor', verbose_name='Donor', null=True)
    url = models.URLField('Url', default='', unique=True)
    title = models.CharField('Title', max_length=500, default='')
    fileName = models.CharField('File Name', max_length=500, default='')
    fileDigest = models.CharField('File Digest', max_length=50, default='', unique=True)
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'I.3 Articles'
    def __unicode__(self):
        return self.title
    def GetNiche(self):
        return self.donor.niche
    GetNiche.short_description = 'Niche'
    GetNiche.allow_tags = True
    def GetSitesCount(self):
        return GetCounter(self.site_set, {'active': True})
    GetSitesCount.short_description = 'Sites'
    GetSitesCount.allow_tags = True

class Hosting(BaseSapeObject):
    '''Хостинг'''
    name = models.CharField('Name', max_length=50, default='')
    mainUrl = models.URLField('Main Url', default='', blank=True)
    controlUrl = models.URLField('Control Url', default='', blank=True)
    billingUrl = models.URLField('Billing Url', default='', blank=True)
    ns1 = models.CharField('NS1', max_length=50, default='', blank=True)
    ns2 = models.CharField('NS2', max_length=50, default='', blank=True)
    rootDocumentTemplate = models.CharField('Document Path', max_length=200, default='')
    class Meta:
        verbose_name = 'Hosting'
        verbose_name_plural = 'II.1 # Hostings'
    def __unicode__(self):
        return self.name
    def GetAccountsCount(self):
        return GetCounter(self.hostingaccount_set, {'active': True})
    GetAccountsCount.short_description = 'Accounts'
    GetAccountsCount.allow_tags = True
    def GetSitesCount(self):
        return GetCounter(self.site_set, {'active': True})  # !!!
    GetSitesCount.short_description = 'Sites'
    GetSitesCount.allow_tags = True
    
class HostingAccount(BaseSapeObject):
    '''Аккаунт на хостинге'''
    hosting = models.ForeignKey('Hosting', verbose_name='Hosting', null=True)
    login = models.CharField('Login', max_length=50, default='')
    password = models.CharField('Password', max_length=50, default='')
    ns1 = models.CharField('NS1', max_length=50, default='', blank=True)
    ns2 = models.CharField('NS2', max_length=50, default='', blank=True)
    costPerMonth = models.FloatField('Cost/month, rub.', null=True, blank=True)
    paidTill = models.DateField('Paid till', null=True, blank=True)
    class Meta:
        verbose_name = 'Hosting Account'
        verbose_name_plural = 'II.2 Hosting Accounts'
    def __unicode__(self):
        return self.login
    def GetSitesCount(self):
        return GetCounter(self.site_set, {'active': True})
    GetSitesCount.short_description = 'Sites'
    GetSitesCount.allow_tags = True

class Site(BaseSapeObject):
    '''Сайт с доменом'''
    niche = models.ForeignKey('Niche', verbose_name='Niche', null=True)
    articles = models.ManyToManyField('Article', verbose_name='Articles', symmetrical=False, null=True, blank=True)
    pagesCount = models.IntegerField('Pages', default=random.randint(200,300), blank=True)
    url = models.CharField('URL', max_length=50, unique=True)
    ipAddress = models.IPAddressField('IP Address', null=True, blank=True)
    hostingAccount = models.ForeignKey('HostingAccount', verbose_name='Hosting Acc.', null=True, blank=True)
    spamTask = models.ForeignKey('SpamTask', verbose_name='Spam Task', null=True, blank=True)
    sapeAccount = models.ForeignKey('SapeAccount', verbose_name='Sape Acc.', null=True, blank=True)
    linksIndexCount = models.IntegerField('L.i.', null=True, default=0, blank=True)  # Links Index
    linksIndexDate = models.DateField('L.i. date', null=True, blank=True)  # Links Index Date
    botsVisitsCount = models.IntegerField('B.v.', null=True, default=0, blank=True)  # Bots Visits
    botsVisitsDate = models.DateField('B.v. date', null=True, blank=True)  # Bots Visits Date
    siteIndexCount = models.IntegerField('S.i.', null=True, default=0, blank=True)  # Site Index 
    siteIndexDate = models.DateField('S.i. date', null=True, blank=True)  # Site Index Date
    state = models.CharField('State', max_length=50, choices=siteStates, default='new', blank=True)
    bulkAddSites = models.TextField('More Sites', default='', blank=True)
    class Meta:
        verbose_name = 'Site'
        verbose_name_plural = 'III.1 # Sites - [large]'
    def __unicode__(self):
        return self.url
    def GetUrl(self):
        if self.state == 'generated':
            return '<a href="%s/out%d" target="_blank">%s</a>' % (vpbblUrl, self.pk, self.url)
        else:
            return '<a href="http://%s" target="_blank">%s</a>' % (self.url, self.url)
    GetUrl.short_description = 'Url'
    GetUrl.allow_tags = True
    def GetSpamDate(self):
        return self.spamTask.spamDate
    GetSpamDate.short_description = 'Spam Date'
    GetSpamDate.allow_tags = True
    def GetLinksIndexCount(self):
        return '<a href="http://blogs.yandex.ru/search.xml?link=%s&noreask=1" target="_blank">%d</a>' % (self.url.replace('http://', 'http%3A%2F%2F'), self.linksIndexCount)
    GetLinksIndexCount.short_description = 'L.i.'
    GetLinksIndexCount.allow_tags = True
    def GetBotsVisitsCount(self):
        return '<a href="http://%s/bots.php" target="_blank">%d</a>&nbsp;<span style="font-size: 10px;">(%.0f%%)</span>' % (self.url, self.botsVisitsCount, float(self.botsVisitsCount) / self.pagesCount * 100)
    GetBotsVisitsCount.short_description = 'B.v.'
    GetBotsVisitsCount.allow_tags = True
    def GetSiteIndexCount(self):
        return '<a href="http://yandex.ru/yandsearch?text=site%%3A%s&lr=2" target="_blank">%d</a>&nbsp;<span style="font-size: 10px;">(%.0f%%)</span>' % (self.url, self.siteIndexCount, float(self.siteIndexCount) / self.pagesCount * 100)
    GetSiteIndexCount.short_description = 'S.i.'
    GetSiteIndexCount.allow_tags = True
    def save(self, *args, **kwargs):
        '''Групповое добавление сайтов с теми же параметрами'''
        if self.bulkAddSites != '':
            for url in self.bulkAddSites.lower().splitlines():
                if url != '':
                    try:
                        site = Site.objects.create(url=url,
                                                   niche=self.niche, 
                                                   pagesCount=random.randint(200,300),
                                                   ipAddress=self.ipAddress,
                                                   hostingAccount=self.hostingAccount)
                        site.save()
                    except Exception:
                        pass
        '''Всегда очищаем поле группового добавления сайтов'''
        self.bulkAddSites = ''
        super(Site, self).save(*args, **kwargs)
    def Generate(self):
        '''Генерация сайта с заливкой на хостинг.
        Генерируем сайты только в статусах "new" и "generated"'''
        if not (self.state in ['new', 'generated']):
            return
        '''Подбираем и выгружаем статьи'''
        self.articles.clear()
        with codecs.open(vpbblLocal + '/text/gen.txt', 'w', 'cp1251') as fd1:
            isFirst = True
            for article in Article.objects.filter(Q(active=True), Q(donor__niche=self.niche)).order_by('?').all()[:self.pagesCount]:
                '''Читаем статью'''
                with open(article.fileName, 'r') as fd2:
                    content = fd2.read().decode('utf8').replace('\n', '').replace('\r', '')
                '''Разбиваем на заголовок и абзацы'''
                sentences = content.split('. ')
                content = sentences[0].strip() + '\r\n'
                sentences = sentences[1:]
                while len(sentences) > 0:
                    n = random.randint(3, 7)
                    content += '<p>' + '. '.join(sentences[:n]) + '.</p>'
                    sentences = sentences[n:]
                '''Добавляем статью в сайт'''
                self.articles.add(article)
                '''Пишем статью в файл'''
                if not isFirst:
                    fd1.write('\r\n<razdelitel>\r\n')
                isFirst = False
                with open(article.fileName, 'r') as fd2:
                    fd1.write(content)
        self.save()
        '''Генерируем сайт'''
        localFolder1 = vpbblLocal + '/out'
        localFolder2 = vpbblLocal + '/out%d' % self.pk
        if not os.path.exists(localFolder1):
            os.mkdir(localFolder1)
            os.system('chmod 777 %s' % localFolder1)
        try:
            templates = [item.replace(vpbblLocal + '/done/', '') for item in glob.glob(vpbblLocal + '/done/*')]
            fd = urllib.urlopen(vpbblUrl + '/include/parse.php?view=zip&q=text%2Fgen.txt&nn=&count=&sin=no&trans=no&picture=no&names=rand&type=html&pre=&onftp=&mymenu=&tpl=' + random.choice(templates))
            fd.read()
            fd.close()
        except Exception:
            pass
        '''Перемещаем в другую папку'''
        if os.path.exists(localFolder2):
            if os.path.isdir(localFolder2):
                shutil.rmtree(localFolder2)
            else:
                os.remove(localFolder2)
        os.rename(localFolder1, localFolder2)
        '''Меняем статус сайта'''
        self.state = 'generated'
        self.save()
    def ChangeIndexPage(self):
        '''Меняем главную страницу'''
        localFolder = vpbblLocal + '/out%d' % self.pk
        if not os.path.exists(localFolder):
            return False
        fileNames = [item for item in os.listdir(localFolder) if item.endswith('.php') and item not in ['index.php', 'map.php', 'codxxx.php', 'botsxxx.php']]
        fileName1 = os.path.join(localFolder, 'index.php')
        fileName2 = os.path.join(localFolder, random.choice(fileNames))
        contents1 = open(fileName1, 'r').read()
        contents2 = open(fileName2, 'r').read()
        open(fileName1, 'w').write(contents2.replace("<? include('codxxx.php'); ?>", "<? include('codxxx.php'); ?> <? include('map.php'); ?>"))
        open(fileName2, 'w').write(contents1.replace("<? include('codxxx.php'); ?> <? include('map.php'); ?>", "<? include('codxxx.php'); ?>"))
        return True
    def Upload(self):
        '''Загружаем на FTP'''
        localFolder = vpbblLocal + '/out%d' % self.pk
        remoteFolder = self.hostingAccount.hosting.rootDocumentTemplate % self.url
        ftp = ftplib.FTP(self.url, self.hostingAccount.login, self.hostingAccount.password)
        try:
            for root, _, files in os.walk(localFolder):
                remoteFolderAdd = ''
                if root != localFolder:
                    remoteFolderAdd = root.replace(localFolder, '')
                    try:
                        ftp.mkd(remoteFolder + remoteFolderAdd)
                    except Exception:
                        pass
                for fname in files:
                    ftp.storbinary('STOR ' + remoteFolder + remoteFolderAdd + '/' + fname, open(os.path.join(root, fname), 'rb'))
        except Exception:
            pass
        '''Устанавливаем права'''
        try:
            ftp.sendcmd('SITE CHMOD 0777 ' + remoteFolder + '/xxx')
            ftp.sendcmd('SITE CHMOD 0777 ' + remoteFolder + '/botsxxx.dat')
        except Exception:
            pass
        ftp.quit()
        '''Удаляем локальную папку'''
        shutil.rmtree(localFolder)
        '''Меняем статус сайта'''
        self.state = 'uploaded'
        self.save()
    def CheckBotVisits(self):
        '''Проверка захода ботов'''
        fd = urllib.urlopen('http://%s/bots.php' % self.url)
        visitsCount = 0
        try:
            visitsCount = int(re.search(r'<b>(\d*)</b>', fd.read(), re.MULTILINE).group(1))
        except Exception:
            pass
        fd.close()
        self.botsVisitsCount = visitsCount
        if (self.botsVisitsDate == None) and (float(visitsCount) / self.pagesCount >= 0.85):
            self.botsVisitsDate = datetime.datetime.now()
        if visitsCount >= self.pagesCount:
            self.state = 'bot-visited'
        self.save()
    def UpdateIndexCount(self):
        '''Проверяем индекс в яндексе'''
        self.siteIndexCount = yandex.GetIndex(self.url)
        self.siteIndexDate = datetime.datetime.now()
        self.save()

class SpamTask(BaseSapeObject):
    '''Задание на спам'''
    spamDate = models.DateField('Spam Date', null=True, blank=True)
    spamLinks = models.TextField('Spammed Links', null=True, blank=True)
    state = models.CharField('State', max_length=50, choices=spamStates, default='')
    class Meta:
        verbose_name = 'Spam Task'
        verbose_name_plural = 'III.2 Spam Tasks'
    def __unicode__(self):
        return '#%s' % self.pk
    def GetSitesCount(self):
        return GetCounter(self.site_set, {'active': True})
    GetSitesCount.short_description = 'Sites'
    GetSitesCount.allow_tags = True

class SapeAccount(BaseSapeObject):
    '''Аккаунт в Sape'''
    login = models.CharField('Login', unique=True, max_length=50, default='')
    password = models.CharField('Password', max_length=50, default='')
    email = models.CharField('Email', max_length=50, default='', blank=True)
    hash = models.CharField('Hash code', max_length=50, default='', blank=True)
    maxSitesCount = models.IntegerField('Max Sites', default=random.randint(70,100))
    WMR = models.ForeignKey('WMR', verbose_name='WMR', null=True, blank=True)
    class Meta:
        verbose_name = 'Sape Account'
        verbose_name_plural = 'IV.1 # Sape Accounts'
    def __unicode__(self):
        return self.login
    def GetSitesCount(self):
        return GetCounter(self.site_set, {'active': True})
    GetSitesCount.short_description = 'Sites'
    GetSitesCount.allow_tags = True

class WMID(BaseSapeObject):
    '''Аккаунт WebMoney'''
    WMID = models.CharField('WMID', max_length=50, default='')
    class Meta:
        verbose_name = 'WMID'
        verbose_name_plural = 'IV.2 WMIDs'
    def __unicode__(self):
        return self.WMID
    def GetWMRsCount(self):
        return GetCounter(self.wmr_set, {'active': True})
    GetWMRsCount.short_description = 'WMRs'
    GetWMRsCount.allow_tags = True

class WMR(BaseSapeObject):
    '''Кошелек WebMoney'''
    WMID = models.ForeignKey('WMID', verbose_name='WMID', null=True)
    WMR = models.CharField('WMR', max_length=50, default='')
    class Meta:
        verbose_name = 'WMR'
        verbose_name_plural = 'IV.3 WMRs'
    def __unicode__(self):
        return self.WMR
    def GetAccountsCount(self):
        return GetCounter(self.sapeaccount_set, {'active': True})
    GetAccountsCount.short_description = 'Accounts'
    GetAccountsCount.allow_tags = True

class YandexUpdate(BaseSapeObject):
    '''Текстовый апдейт Яндекса'''
    dateIndex = models.DateField('Index Date', unique=True)
    dateUpdate = models.DateField('Update Date')
    class Meta:
        verbose_name = 'Yandex Update'
        verbose_name_plural = 'V.1 # Yandex Updates'
    def __unicode__(self):
        return str(self.dateUpdate)
