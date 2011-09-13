# coding=utf8
from django.contrib import admin
from sapeadmin.models import *
from django.contrib.admin.actions import delete_selected
import yandex
delete_selected.short_description = '9. Delete selected items'

def GetMessageBit(rows_updated):
    '''Текст для сообщений'''
    if rows_updated == 0:
        return "No items were"
    elif rows_updated == 1:
        return "1 item was successfully"
    else:
        return "%s items were successfully" % rows_updated

'''Базовые классы'''

class BaseAdmin(admin.ModelAdmin):
    list_per_page = 20
    readonly_fields = ['dateAdded', 'dateChanged']

class BaseAdminActivatable(BaseAdmin):
    actions = ['MakeActive', 'MakeInactive']
    def MakeActive(self, request, queryset):
        rows_updated = queryset.update(active=True)
        self.message_user(request, "%s enabled." % GetMessageBit(rows_updated))
    MakeActive.short_description = "1. Enable selected items"
    def MakeInactive(self, request, queryset):
        rows_updated = queryset.update(active=False)
        self.message_user(request, "%s disabled." % GetMessageBit(rows_updated))
    MakeInactive.short_description = "2. Disable selected items"
    
'''Реальные классы'''

class NicheAdmin(BaseAdminActivatable):
    list_display = ('pk', 'priority', 'name', 'GetDonorsCount', 'GetArticlesCount', 'GetSitesCount', 'active', 'dateAdded')
    ordering = ['priority']
    fieldsets = [
        (None, {'fields': [('name', 'priority')]}),
        ('Information', {'fields': ['remarks', ('dateAdded', 'dateChanged', 'active')], 'classes': ['collapse']}),
    ]

class DonorAdmin(BaseAdminActivatable):
    list_display = ('pk', 'niche', 'GetUrl', 'GetArticlesCount', 'active', 'dateAdded')
    list_filter = ['niche']
    ordering = ['niche', 'url']
    search_fields = ['url']
    fieldsets = [
        (None, {'fields': ['niche', 'url']}),
        ('Information', {'fields': ['remarks', ('dateAdded', 'dateChanged', 'active')], 'classes': ['collapse']}),
    ]

class ArticleAdmin(BaseAdminActivatable):
    list_display = ('pk', 'GetNiche', 'donor', 'title', 'GetSitesCount', 'active', 'dateAdded')
    list_filter = ['donor__niche', 'donor']
    ordering = ['donor__niche', 'donor', 'title']
    search_fields = ['title']
    fieldsets = [
        (None, {'fields': ['donor', 'url', 'title', 'fileName']}),
        ('Information', {'fields': ['remarks', ('dateAdded', 'dateChanged', 'active')], 'classes': ['collapse']}),
    ]

class HostingAdmin(BaseAdminActivatable):
    list_display = ('pk', 'name', 'active', 'GetAccountsCount', 'GetSitesCount', 'dateAdded')
    ordering = ['name']
    fieldsets = [
        (None, {'fields': ['name', 'mainUrl', ('controlUrl', 'billingUrl'), ('ns1', 'ns2'), ('rootDocumentTemplate')]}),
        ('Information', {'fields': ['remarks', ('dateAdded', 'dateChanged', 'active')], 'classes': ['collapse']}),
    ]
    
class HostingAccountAdmin(BaseAdminActivatable):
    list_display = ('pk', 'hosting', 'login', 'costPerMonth', 'paidTill', 'GetSitesCount', 'active', 'dateAdded')
    list_filter = ['hosting']
    ordering = ['hosting', 'login']
    fieldsets = [
        (None, {'fields': ['hosting', ('login', 'password'), ('ns1', 'ns2'), ('costPerMonth', 'paidTill')]}),
        ('Information', {'fields': ['remarks', ('dateAdded', 'dateChanged', 'active')], 'classes': ['collapse']}),
    ]

class SiteAdmin(BaseAdmin):
    list_display = ('pk', 'niche', 'GetUrl', 'pagesCount', 'GetSpamDate', 'GetLinksIndexCount', 'linksIndexDate', 'GetBotsVisitsCount', 'botsVisitsDate', 'GetSiteIndexCount', 'siteIndexDate', 'sapeAccount', 'state', 'active', 'dateAdded')
    list_filter = ['state', 'niche', 'hostingAccount', 'sapeAccount']
    search_fields = ['url']
    fieldsets = [
        (None, {'fields': [('niche', 'state'), ('url', 'pagesCount'), ('hostingAccount', 'spamTask', 'sapeAccount'), ('linksIndexCount', 'linksIndexDate'), ('botsVisitsCount', 'botsVisitsDate'), ('siteIndexCount', 'siteIndexDate')]}),
        ('Bulk add sites', {'fields': [('bulkAddSites')], 'classes': ['expanded']}),
        ('Information', {'fields': ['remarks', ('dateAdded', 'dateChanged', 'active')], 'classes': ['collapse']}),
    ]
    actions = ['MakeStateNew', 'MakeStateSapeAdded', 'MakeStateSapeApproved', 
               'MakeStateSapePrice1', 'MakeStateSapePrice2', 'MakeStateSapePrice3', 'MakeStateSapeBanned',
               'Generate', 'ChangeIndexPage', 'Upload', 'CheckBotVisits', 'UpdateIndexCount']
    def MakeStateNew(self, request, queryset):
        rows_updated = queryset.update(state='new')
        self.message_user(request, "%s marked as new." % GetMessageBit(rows_updated))
    MakeStateNew.short_description = "1. Mark selected items as new"
    def MakeStateSapeAdded(self, request, queryset):
        rows_updated = queryset.update(state='sape-added')
        self.message_user(request, "%s marked as sape-added." % GetMessageBit(rows_updated))
    MakeStateSapeAdded.short_description = "2. Mark selected items as sape-added"
    def MakeStateSapeApproved(self, request, queryset):
        rows_updated = queryset.update(state='sape-approved')
        self.message_user(request, "%s marked as sape-approved." % GetMessageBit(rows_updated))
    MakeStateSapeApproved.short_description = "3. Mark selected items as sape-approved"
    def MakeStateSapePrice1(self, request, queryset):
        rows_updated = queryset.update(state='sape-price1')
        self.message_user(request, "%s marked as sape-price1." % GetMessageBit(rows_updated))
    MakeStateSapePrice1.short_description = "4. Mark selected items as sape-price1"
    def MakeStateSapePrice2(self, request, queryset):
        rows_updated = queryset.update(state='sape-price2')
        self.message_user(request, "%s marked as sape-price2." % GetMessageBit(rows_updated))
    MakeStateSapePrice2.short_description = "5. Mark selected items as sape-price2"
    def MakeStateSapePrice3(self, request, queryset):
        rows_updated = queryset.update(state='sape-price3')
        self.message_user(request, "%s marked as sape-price3." % GetMessageBit(rows_updated))
    MakeStateSapePrice3.short_description = "6. Mark selected items as sape-price3"
    def MakeStateSapeBanned(self, request, queryset):
        rows_updated = queryset.update(state='sape-banned')
        self.message_user(request, "%s marked as sape-banned." % GetMessageBit(rows_updated))
    MakeStateSapeBanned.short_description = "7. Mark selected items as sape-banned"
    def Generate(self, request, queryset):
        '''Генерируем сайты'''
        processed = 0
        for site in queryset:
            site.Generate()
            processed += 1
        self.message_user(request, "%s generated." % GetMessageBit(processed))
    Generate.short_description = "a. Generate site"
    def ChangeIndexPage(self, request, queryset):
        '''Меняем главную страницу'''
        processed = 0
        for site in queryset:
            site.ChangeIndexPage()
            processed += 1
        self.message_user(request, "%s changed." % GetMessageBit(processed))
    ChangeIndexPage.short_description = "b. Change index page"
    def Upload(self, request, queryset):
        '''Загружаем на FTP'''
        processed = 0
        for site in queryset:
            site.Upload()
            processed += 1
        self.message_user(request, "%s uploaded." % GetMessageBit(processed))
    Upload.short_description = "c. Upload site to FTP"
    def CheckBotVisits(self, request, queryset):
        '''Проверяем посещение сайтов ботами'''
        processed = 0
        for site in queryset:
            site.CheckBotVisits()
            processed += 1
        self.message_user(request, "%s checked." % GetMessageBit(processed))
    CheckBotVisits.short_description = "d. Check bots visits"
    def UpdateIndexCount(self, request, queryset):
        '''Проверяем индекс в яндексе'''
        processed = 0
        yandex.Initialize()
        for site in queryset:
            site.UpdateIndexCount()
            processed += 1
        self.message_user(request, "%s checked." % GetMessageBit(processed))
    UpdateIndexCount.short_description = "e. Check Yandex index"

class SpamTaskAdmin(BaseAdmin):
    list_display = ('pk', 'spamDate', 'GetSitesCount', 'state', 'active', 'dateAdded')
    list_filter = ['state']
    fieldsets = [
        (None, {'fields': [('spamDate', 'state'), 'spamLinks']}),
        ('Information', {'fields': ['remarks', ('dateAdded', 'dateChanged', 'active')], 'classes': ['collapse']}),
    ]

class SapeAccountAdmin(BaseAdminActivatable):
    list_display = ('pk', 'login', 'maxSitesCount', 'WMR', 'GetSitesCount', 'active', 'dateAdded')
    list_filter = ['WMR']
    fieldsets = [
        (None, {'fields': [('login', 'password', 'email'), 'hash', ('maxSitesCount', 'WMR')]}),
        ('Information', {'fields': ['remarks', ('dateAdded', 'dateChanged', 'active')], 'classes': ['collapse']}),
    ]

class WMIDAdmin(BaseAdmin):
    list_display = ('pk', 'WMID', 'GetWMRsCount', 'active', 'dateAdded')
    ordering = ['WMID']
    fieldsets = [
        (None, {'fields': ['WMID']}),
        ('Information', {'fields': ['remarks', ('dateAdded', 'dateChanged', 'active')], 'classes': ['collapse']}),
    ]

class WMRAdmin(BaseAdmin):
    list_display = ('pk', 'WMID', 'WMR', 'GetAccountsCount', 'active', 'dateAdded')
    list_filter = ['WMID']
    ordering = ['WMR']
    fieldsets = [
        (None, {'fields': [('WMID', 'WMR')]}),
        ('Information', {'fields': ['remarks', ('dateAdded', 'dateChanged', 'active')], 'classes': ['collapse']}),
    ]

class YandexUpdateAdmin(BaseAdmin):
    list_display = ('pk', 'dateIndex', 'dateUpdate')
    fieldsets = [
        (None, {'fields': [('dateIndex', 'dateUpdate')]}),
        ('Information', {'fields': ['remarks', ('dateAdded', 'dateChanged', 'active')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['dateIndex', 'dateUpdate', 'dateAdded', 'dateChanged']

admin.site.register(Niche, NicheAdmin)
admin.site.register(Donor, DonorAdmin)
admin.site.register(Article, ArticleAdmin)

admin.site.register(Hosting, HostingAdmin)
admin.site.register(HostingAccount, HostingAccountAdmin)

admin.site.register(Site, SiteAdmin)

admin.site.register(SapeAccount, SapeAccountAdmin)
admin.site.register(SpamTask, SpamTaskAdmin)
admin.site.register(WMID, WMIDAdmin)
admin.site.register(WMR, WMRAdmin)

admin.site.register(YandexUpdate, YandexUpdateAdmin)
