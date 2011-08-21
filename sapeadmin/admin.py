# coding=utf8
from django.contrib import admin
from sapeadmin.models import *
from django.contrib.admin.actions import delete_selected
delete_selected.short_description = '9. Delete selected items'

def GetMessageBit(rows_updated):
    '''Текст для сообщений'''
    if rows_updated == 1:
        return "1 item was"
    else:
        return "%s items were" % rows_updated

'''Базовые классы'''

class BaseAdmin(admin.ModelAdmin):
    list_per_page = 20
    readonly_fields = ['dateAdded', 'dateChanged']
    actions = ['MakeActive', 'MakeInactive']
    def MakeActive(self, request, queryset):
        rows_updated = queryset.update(active=True)
        self.message_user(request, "%s successfully enabled." % GetMessageBit(rows_updated))
    MakeActive.short_description = "1. Enable selected items"
    def MakeInactive(self, request, queryset):
        rows_updated = queryset.update(active=False)
        self.message_user(request, "%s successfully disabled." % GetMessageBit(rows_updated))
    MakeInactive.short_description = "2. Disable selected items"

'''Реальные классы'''

class NicheAdmin(BaseAdmin):
    list_display = ('pk', 'priority', 'name', 'GetDonorsCount', 'GetArticlesCount', 'GetSitesCount', 'active', 'dateAdded')
    ordering = ['priority']
    fieldsets = [
        (None, {'fields': [('name', 'priority')]}),
        ('Information', {'fields': ['remarks', ('dateAdded', 'dateChanged', 'active')], 'classes': ['collapse']}),
    ]

class DonorAdmin(BaseAdmin):
    list_display = ('pk', 'niche', 'GetUrl', 'GetArticlesCount', 'active', 'dateAdded')
    list_filter = ['niche']
    ordering = ['niche', 'url']
    search_fields = ['url']
    fieldsets = [
        (None, {'fields': ['niche', 'url']}),
        ('Information', {'fields': ['remarks', ('dateAdded', 'dateChanged', 'active')], 'classes': ['collapse']}),
    ]

class ArticleAdmin(BaseAdmin):
    list_display = ('pk', 'niche', 'donor', 'title', 'GetSitesCount', 'active', 'dateAdded')
    list_filter = ['niche', 'donor']
    ordering = ['niche', 'donor', 'title']
    search_fields = ['title']
    fieldsets = [
        (None, {'fields': [('niche', 'donor'), 'title', 'textFile']}),
        ('Information', {'fields': ['remarks', ('dateAdded', 'dateChanged', 'active')], 'classes': ['collapse']}),
    ]

class HostingAdmin(BaseAdmin):
    list_display = ('pk', 'name', 'active', 'GetAccountsCount', 'GetSitesCount', 'dateAdded')
    ordering = ['name']
    fieldsets = [
        (None, {'fields': ['name', 'mainUrl', ('controlUrl', 'billingUrl'), ('ns1', 'ns2')]}),
        ('Information', {'fields': ['remarks', ('dateAdded', 'dateChanged', 'active')], 'classes': ['collapse']}),
    ]
    
class HostingAccountAdmin(BaseAdmin):
    list_display = ('pk', 'hosting', 'login', 'costPerMonth', 'paymentDay', 'GetSitesCount', 'active', 'dateAdded')
    list_filter = ['hosting']
    ordering = ['hosting', 'login']
    fieldsets = [
        (None, {'fields': ['hosting', ('login', 'password'), ('ns1', 'ns2'), ('costPerMonth', 'paymentDay')]}),
        ('Information', {'fields': ['remarks', ('dateAdded', 'dateChanged', 'active')], 'classes': ['collapse']}),
    ]

class SiteAdmin(BaseAdmin):
    list_display = ('pk', 'niche', 'GetUrl', 'sapeAccount', 'linksIndexCount', 'botsVisitsCount', 'siteIndexCount', 'state', 'active', 'dateAdded')
    list_filter = ['niche', 'hostingAccount', 'sapeAccount', 'state']
    search_fields = ['url']
    fieldsets = [
        (None, {'fields': [('niche', 'state'), ('url', 'pagesCount'), ('hostingAccount', 'spamTask', 'sapeAccount'), ('linksIndexCount', 'linksIndexDate'), ('botsVisitsCount', 'botsVisitsDate'), ('siteIndexCount', 'siteIndexDate')]}),
        ('Information', {'fields': ['remarks', ('dateAdded', 'dateChanged', 'active')], 'classes': ['collapse']}),
    ]

class SpamTaskAdmin(BaseAdmin):
    list_display = ('pk', 'spamDate', 'GetSitesCount', 'state', 'active', 'dateAdded')
    list_filter = ['state']
    fieldsets = [
        (None, {'fields': [('spamDate', 'state'), 'spamLinks']}),
        ('Information', {'fields': ['remarks', ('dateAdded', 'dateChanged', 'active')], 'classes': ['collapse']}),
    ]

class SapeAccountAdmin(BaseAdmin):
    list_display = ('pk', 'spamTask', 'login', 'maxSitesCount', 'WMR', 'GetSitesCount', 'active', 'dateAdded')
    list_filter = ['WMR']
    fieldsets = [
        (None, {'fields': ['spamTask', ('login', 'password', 'email'), 'hash', ('maxSitesCount', 'WMR')]}),
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
    list_display = ('pk', 'dateUpdate', 'dateIndex')
    fieldsets = [
        (None, {'fields': [('dateUpdate', 'dateIndex')]}),
        ('Information', {'fields': ['remarks', ('dateAdded', 'dateChanged', 'active')], 'classes': ['collapse']}),
    ]

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
