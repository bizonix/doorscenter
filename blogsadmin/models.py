# coding=utf8
from django.db import models
import datetime, engines

class Blog(models.Model):
    '''Блог'''
    domain = models.CharField('Domain', max_length=200, unique=True)
    group = models.CharField('Group', max_length=200, default='', blank=True)
    indexCount = models.IntegerField('GI', null=True, blank=True)
    backLinksCount = models.IntegerField('BL', null=True, blank=True)
    lastChecked = models.DateTimeField('Last Checked', null=True, blank=True)
    bulkAddBlogs = models.TextField('Bulk Add', default='', blank=True)
    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = '1. Blogs'
    def __unicode__(self):
        return self.domain
    def save(self, *args, **kwargs):
        '''Массово добавляем блоги'''
        if self.bulkAddBlogs != '':
            for line in self.bulkAddBlogs.lower().splitlines():
                line = line.strip()
                if line != '':
                    try:
                        Blog.objects.create(domain=line, group=self.group).save()
                    except Exception:
                        pass
        self.bulkAddBlogs = ''
        super(Blog, self).save(*args, **kwargs)
    def GetIndexCount(self):
        '''Ссылка для проверки индекса по гуглу'''
        return '<a href="%s">%s</a>' % (engines.Google.GetIndexLink(self.domain), (str(self.indexCount) if self.indexCount else '-'))
    GetIndexCount.short_description = 'GI'
    GetIndexCount.allow_tags = True
    GetIndexCount.admin_order_field = 'indexCount'
    def GetBackLinksCount(self):
        '''Ссылка для проверки back links'''
        return '<a href="%s">%s</a>' % (engines.Majestic.GetBackLinksLink(self.domain), (str(self.backLinksCount) if self.backLinksCount else '-'))
    GetBackLinksCount.short_description = 'BL'
    GetBackLinksCount.allow_tags = True
    GetBackLinksCount.admin_order_field = 'backLinksCount'
    def Check(self):
        '''Проверяем индекс и ссылки'''
        try:
            self.indexCount = engines.Google.GetIndex(self.domain)
            self.backLinksCount = engines.Majestic.GetBackLinks(self.domain)
            self.lastChecked = datetime.datetime.now()
            self.save()
        except Exception:
            pass

class Position(models.Model):
    '''Кейворды и позиции'''
    blog = models.ForeignKey('Blog', verbose_name='Blog')
    keyword = models.CharField('Keyword', max_length=200, default='')
    group = models.CharField('Group', max_length=200, default='', blank=True)
    googlePosition = models.IntegerField('G.Pos.', null=True, blank=True)
    googleMaxPosition = models.IntegerField('G.Pos.Max.', null=True, blank=True)
    googleMaxPositionDate = models.DateTimeField('G.Pos.Max.Date', null=True, blank=True)
    googleExtendedInfo = models.TextField('Google Info', default='', blank=True)
    yahooPosition = models.IntegerField('Y.Pos.', null=True, blank=True)
    yahooMaxPosition = models.IntegerField('Y.Pos.Max.', null=True, blank=True)
    yahooMaxPositionDate = models.DateTimeField('Y.Pos.Max.Date', null=True, blank=True)
    yahooExtendedInfo = models.TextField('Yahoo Info', default='', blank=True)
    bingPosition = models.IntegerField('B.Pos.', null=True, blank=True)
    bingMaxPosition = models.IntegerField('B.Pos.Max.', null=True, blank=True)
    bingMaxPositionDate = models.DateTimeField('B.Pos.Max.Date', null=True, blank=True)
    bingExtendedInfo = models.TextField('Bing Info', default='', blank=True)
    lastChecked = models.DateTimeField('Last Checked', null=True, blank=True)
    bulkAddKeywords = models.TextField('Bulk Add', default='', blank=True)
    class Meta:
        verbose_name = 'Position'
        verbose_name_plural = '2. Positions'
    def __unicode__(self):
        return '%s: %s' % (self.blog.domain, self.keyword)
    def save(self, *args, **kwargs):
        '''Массово добавляем кейворды'''
        if self.bulkAddKeywords != '':
            for line in self.bulkAddKeywords.lower().splitlines():
                if line != '':
                    try:
                        domain = line.split(':')[0].strip()
                        keyword = line.split(':')[1].strip()
                        blog, _ = Blog.objects.get_or_create(domain=domain)
                        Position.objects.create(blog=blog, keyword=keyword, group=self.group).save()
                    except Exception:
                        pass
        self.bulkAddKeywords = ''
        super(Position, self).save(*args, **kwargs)
    def GetGooglePosition(self):
        '''Ссылка для проверки позиции в гугле'''
        return '<a href="%s">%s</a>' % (engines.Google.GetPositionLink(self.keyword), (str(self.googlePosition) if self.googlePosition else '-'))
    GetGooglePosition.short_description = 'G.Pos.'
    GetGooglePosition.allow_tags = True
    GetGooglePosition.admin_order_field = 'googlePosition'
    def GetYahooPosition(self):
        '''Ссылка для проверки позиции в яху'''
        return '<a href="%s">%s</a>' % (engines.Yahoo.GetPositionLink(self.keyword), (str(self.yahooPosition) if self.yahooPosition else '-'))
    GetYahooPosition.short_description = 'Y.Pos.'
    GetYahooPosition.allow_tags = True
    GetYahooPosition.admin_order_field = 'yahooPosition'
    def GetBingPosition(self):
        '''Ссылка для проверки позиции в бинг'''
        return '<a href="%s">%s</a>' % (engines.Bing.GetPositionLink(self.keyword), (str(self.bingPosition) if self.bingPosition else '-'))
    GetBingPosition.short_description = 'B.Pos.'
    GetBingPosition.allow_tags = True
    GetBingPosition.admin_order_field = 'bingPosition'
    def Check(self):
        '''Проверяем позиции'''
        try:
            self.googlePosition, self.googleExtendedInfo = engines.Google.GetPosition(self.blog.domain, self.keyword)
            if (self.googlePosition) and (self.googlePosition <= (self.googleMaxPosition if self.googleMaxPosition != None else 101)):
                self.googleMaxPosition = self.googlePosition
                self.googleMaxPositionDate = datetime.datetime.now()
            self.yahooPosition, self.yahooExtendedInfo = engines.Yahoo.GetPosition(self.blog.domain, self.keyword)
            if (self.yahooPosition) and (self.yahooPosition <= (self.yahooMaxPosition if self.yahooMaxPosition != None else 101)):
                self.yahooMaxPosition = self.yahooPosition
                self.yahooMaxPositionDate = datetime.datetime.now()
            self.bingPosition, self.bingExtendedInfo = engines.Bing.GetPosition(self.blog.domain, self.keyword)
            if (self.bingPosition) and (self.bingPosition <= (self.bingMaxPosition if self.bingMaxPosition != None else 101)):
                self.bingMaxPosition = self.bingPosition
                self.bingMaxPositionDate = datetime.datetime.now()
            self.lastChecked = datetime.datetime.now()
            self.save()
        except Exception:
            pass
