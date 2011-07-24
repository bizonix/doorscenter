# coding=utf8
from django.contrib import admin
from doorsadmin.models import *
from django.contrib.admin.actions import delete_selected
delete_selected.short_description = '9. Delete selected items'

class BaseAdmin(admin.ModelAdmin):
    list_per_page = 20

def GetMessageBit(rows_updated):
    '''Текст для сообщений'''
    if rows_updated == 1:
        return "1 item was"
    else:
        return "%s items were" % rows_updated

class BaseAdminActivatable(BaseAdmin):
    actions = ['MakeActive', 'MakeInactive']
    def MakeActive(self, request, queryset):
        rows_updated = queryset.update(active=True)
        self.message_user(request, "%s successfully enabled." % GetMessageBit(rows_updated))
    MakeActive.short_description = "1. Enable selected items"
    def MakeInactive(self, request, queryset):
        rows_updated = queryset.update(active=False)
        self.message_user(request, "%s successfully disabled." % GetMessageBit(rows_updated))
    MakeInactive.short_description = "2. Disable selected items"

class BaseAdminManaged(BaseAdmin):
    actions = ['MakeStateManagedNew', 'MakeStateManagedDone', 'MakePriorityHigh', 'MakePriorityStd', 'MakePriorityZero']
    def MakeStateManagedNew(self, request, queryset):
        rows_updated = queryset.update(stateManaged='new')
        self.message_user(request, "%s successfully marked as new." % GetMessageBit(rows_updated))
    MakeStateManagedNew.short_description = "3. Mark selected items as new"
    def MakeStateManagedDone(self, request, queryset):
        rows_updated = queryset.update(stateManaged='done')
        self.message_user(request, "%s successfully marked as done." % GetMessageBit(rows_updated))
    MakeStateManagedDone.short_description = "4. Mark selected items as done"
    def MakePriorityHigh(self, request, queryset):
        rows_updated = queryset.update(priority='high')
        self.message_user(request, "%s successfully marked as priority high." % GetMessageBit(rows_updated))
    MakePriorityHigh.short_description = "5. Mark selected items as priority high"
    def MakePriorityStd(self, request, queryset):
        rows_updated = queryset.update(priority='std')
        self.message_user(request, "%s successfully marked as priority std." % GetMessageBit(rows_updated))
    MakePriorityStd.short_description = "6. Mark selected items as priority std"
    def MakePriorityZero(self, request, queryset):
        rows_updated = queryset.update(priority='zero')
        self.message_user(request, "%s successfully marked as priority zero." % GetMessageBit(rows_updated))
    MakePriorityZero.short_description = "7. Mark selected items as priority zero"

class BaseAdminSimple(BaseAdmin):
    actions = ['MakeStateSimpleOk']
    def MakeStateSimpleOk(self, request, queryset):
        rows_updated = queryset.update(stateSimple='ok')
        self.message_user(request, "%s successfully marked as ok." % GetMessageBit(rows_updated))
    MakeStateSimpleOk.short_description = "3. Mark selected items as ok"

'''Agents'''

class AgentAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'type', 'description', 'currentTask', 'GetTasksState', 'GetDateLastPingAgo', 'interval', 'active', 'stateSimple', 'dateAdded')
    list_filter = ['active', 'stateSimple']
    fieldsets = [
        (None, {'fields': ['type', 'description', ('currentTask', 'dateLastPing', 'interval'), 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['currentTask', 'dateLastPing', 'lastError', 'dateAdded', 'dateChanged']

class EventAdmin(BaseAdmin):
    list_display = ('pk', 'date', 'type', 'object', 'text')
    list_filter = ['type']
    fieldsets = [
        (None, {'fields': ['date', ('type', 'object'), 'text']}),
    ]
    readonly_fields = ['date', 'type', 'object', 'text']

'''Domains group'''

class DomainAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'GetDomainUrl', 'net', 'niche', 'host', 'dateRegistered', 'GetDoorsMaxCount', 'GetPagesCount', 'active', 'stateSimple', 'dateAdded')
    list_filter = ['active', 'net', 'niche', 'stateSimple']
    search_fields = ['name']
    fieldsets = [
        (None, {'fields': ['name', ('net', 'niche', 'host', 'maxDoorsCount'), 'active']}),
        ('Net', {'fields': [('linkedDomains')], 'classes': ['expanded']}),
        ('Addresses', {'fields': [('ipAddress', 'nameServer1', 'nameServer2', 'useOwnDNS')], 'classes': ['expanded']}),
        ('Dates', {'fields': [('dateRegistered', 'dateExpires')], 'classes': ['expanded']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']
    
class NetAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'description', 'niche', 'makeSpam', 'piwikId', 'GetDomainsCount', 'minPagesCount', 'maxPagesCount', 'GetSchedulesCount', 'GetDoorsCount', 'GetPagesCount', 'active', 'stateSimple', 'dateAdded')
    list_filter = ['active', 'niche', 'stateSimple']
    ordering = ['description']
    fieldsets = [
        (None, {'fields': ['description', ('niche', 'keywordsSet', 'template', 'doorgenProfile'), ('minPagesCount', 'maxPagesCount', 'minSpamLinksPercent', 'maxSpamLinksPercent'), 'settings', ('active', 'makeSpam', 'generateNow')]}),
        ('Analytics', {'fields': [('piwikId', 'analyticsId')], 'classes': ['expanded']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']
    list_per_page = 100

class HostAdmin(BaseAdminSimple):
    list_display = ('pk', 'type', 'company', 'hostName', 'costPerMonth', 'diskSpace', 'traffic', 'controlPanelType', 'GetIPAddressesCount', 'GetDomainsCount', 'GetDoorsCount', 'GetPagesCount', 'stateSimple', 'dateAdded')
    list_filter = ['stateSimple']
    fieldsets = [
        (None, {'fields': ['type', ('company', 'hostName'), ('costPerMonth', 'diskSpace', 'traffic'), ('controlPanelType', 'controlPanelUrl', 'controlPanelServerId')]}),
        ('FTP Account', {'fields': [('ftpLogin', 'ftpPassword', 'ftpPort'), 'rootDocumentTemplate'], 'classes': ['expanded']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class IPAddressAdmin(BaseAdminSimple):
    list_display = ('pk', 'address', 'host', 'GetDomainsCount', 'GetDoorsCount', 'GetPagesCount', 'stateSimple', 'dateAdded')
    list_filter = ['stateSimple']
    ordering = ['address']
    fieldsets = [
        (None, {'fields': ['address', 'host']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

'''Doorways group'''
    
class SpamLinkInline(admin.TabularInline):
    model = SpamLink
    extra = 1

class SpamLinkAdmin(BaseAdmin):
    list_display = ('pk', 'url', 'anchor', 'spamTask')
    fieldsets = [
        (None, {'fields': [('url', 'anchor'), ('doorway', 'spamTask')]}),
    ]

class DoorwayAdmin(BaseAdminManaged):
    list_display = ('pk', 'GetNet', 'niche', 'keywordsSet', 'template', 'pagesCount', 'GetSpamLinksCount', 'GetUrl', 'priority', 'GetRunTime', 'stateManaged', 'dateAdded')
    list_filter = ['niche', 'template', 'stateManaged', 'priority']
    search_fields = ['domain__name']
    fieldsets = [
        (None, {'fields': [('niche'), ('keywordsSet', 'template', 'doorgenProfile'), ('domain', 'domainFolder'), ('pagesCount', 'spamLinksCount'), 'doorwaySchedule']}),
        ('Lists', {'fields': ['keywordsList', 'netLinksList'], 'classes': ['expanded']}),
        ('Analytics', {'fields': [('piwikId', 'analyticsId')], 'classes': ['collapse']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['doorwaySchedule', 'lastError', 'dateAdded', 'dateChanged']
    #inlines = [SpamLinkInline]

class NicheAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'description', 'language', 'GetStopWordsCount', 'GetKeywordsSetsCount', 'GetTemplatesCount', 'GetDomainsCount', 'GetSchedulesCount', 'GetDoorsCount', 'GetPagesCount', 'GetSnippetsSetsCount', 'GetXrumerBasesRCount', 'GetSpamLinksCount', 'active', 'stateSimple', 'dateAdded')
    list_filter = ['active', 'language', 'stateSimple']
    ordering = ['description']
    fieldsets = [
        (None, {'fields': ['description', 'language', 'stopwordsList', 'active']}),
        ('Analytics', {'fields': [('piwikId', 'analyticsId')], 'classes': ['expanded']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']
    list_per_page = 50

class KeywordsSetAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'niche', 'GetLocalFolder', 'encoding', 'keywordsCount', 'GetDoorsCount', 'GetPagesCount', 'active', 'stateSimple', 'dateAdded')
    list_filter = ['active', 'niche', 'stateSimple']
    ordering = ['niche__description']
    fieldsets = [
        (None, {'fields': ['niche', ('localFolder', 'keywordsCount', 'encoding'), 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class TemplateAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'niche', 'type', 'localFolder', 'GetDoorsCount', 'GetPagesCount', 'active', 'stateSimple', 'dateAdded')
    list_filter = ['active', 'niche', 'stateSimple']
    ordering = ['niche__description']
    fieldsets = [
        (None, {'fields': [('niche', 'type'), 'localFolder', 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class DoorgenProfileAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'description', 'GetDoorsCount', 'GetPagesCount', 'active', 'stateSimple', 'dateAdded')
    list_filter = ['active', 'stateSimple']
    fieldsets = [
        (None, {'fields': ['description', 'settings', 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class DoorwayScheduleAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'net', 'dateStart', 'dateEnd', 'GetDoorsTodayCount', 'GetDoorsCount', 'GetPagesCount', 'active', 'stateSimple', 'dateAdded')
    list_filter = ['active', 'stateSimple']
    ordering = ['net__niche__description']
    fieldsets = [
        (None, {'fields': ['net', ('dateStart', 'dateEnd', 'doorsPerDay'), 'active']}),
        ('Run', {'fields': [('lastRun', 'doorsToday')], 'classes': ['expand']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastRun', 'doorsToday', 'lastError', 'dateAdded', 'dateChanged']

'''Spam group'''

class SpamTaskAdmin(BaseAdminManaged):
    list_display = ('pk', 'xrumerBaseR', 'snippetsSet', 'successCount', 'halfSuccessCount', 'failsCount', 'priority', 'GetRunTime', 'stateManaged', 'dateAdded')
    list_filter = ['stateManaged', 'priority']
    fieldsets = [
        (None, {'fields': [('xrumerBaseR', 'snippetsSet'), ('successCount', 'halfSuccessCount', 'failsCount', 'profilesCount')]}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['successCount', 'halfSuccessCount', 'failsCount', 'profilesCount', 'lastError', 'dateAdded', 'dateChanged']
    inlines = [SpamLinkInline]

class SnippetsSetAdmin(BaseAdminActivatable, BaseAdminManaged):
    list_display = ('pk', 'niche', 'localFile', 'keywordsCount', 'interval', 'GetDateLastParsedAgo', 'phrasesCount', 'active', 'priority', 'GetRunTime', 'stateManaged', 'dateAdded')
    list_filter = ['active', 'niche', 'stateManaged', 'priority']
    ordering = ['niche__description']
    fieldsets = [
        (None, {'fields': ['niche', ('localFile', 'keywordsCount'), ('interval', 'dateLastParsed'), 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['dateLastParsed', 'lastError', 'dateAdded', 'dateChanged']

class XrumerBaseRawAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('baseNumber', 'description', 'linksCount', 'language', 'GetXrumerBasesRCount', 'active', 'stateSimple', 'dateAdded')
    list_filter = ['active', 'stateSimple']
    fieldsets = [
        (None, {'fields': ['description', ('baseNumber', 'linksCount', 'language'), 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class XrumerBaseRAdmin(BaseAdminActivatable, BaseAdminManaged):
    list_display = ('baseNumber', 'niche', 'linksCount', 'xrumerBaseRaw', 'snippetsSet', 'GetSpamTasksCount', 'successCount', 'halfSuccessCount', 'failsCount', 'active', 'priority', 'GetRunTime', 'stateManaged', 'dateAdded')
    list_filter = ['active', 'niche', 'stateManaged', 'priority']
    ordering = ['niche__description']
    fieldsets = [
        (None, {'fields': [('niche', 'linksCount'), ('baseNumber', 'xrumerBaseRaw', 'snippetsSet'), ('nickName', 'realName', 'password'), ('emailAddress', 'emailLogin'), ('emailPassword', 'emailPopServer'), ('successCount', 'halfSuccessCount', 'failsCount', 'profilesCount'), 'active']}),
        ('Spam parameters', {'fields': [('spamTaskDomainsMin', 'spamTaskDomainsMax', 'nextSpamTaskDomainsCount'), ('spamTaskDomainLinksMin', 'spamTaskDomainLinksMax')], 'classes': ['expanded']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['nickName', 'realName', 'password', 'successCount', 'halfSuccessCount', 'failsCount', 'profilesCount', 'lastError', 'dateAdded', 'dateChanged']

admin.site.register(Agent, AgentAdmin)
admin.site.register(Event, EventAdmin)

admin.site.register(Domain, DomainAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(IPAddress, IPAddressAdmin)

admin.site.register(SpamLink, SpamLinkAdmin)
admin.site.register(Doorway, DoorwayAdmin)
admin.site.register(Niche, NicheAdmin)
admin.site.register(KeywordsSet, KeywordsSetAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(Net, NetAdmin)
admin.site.register(DoorgenProfile, DoorgenProfileAdmin)
admin.site.register(DoorwaySchedule, DoorwayScheduleAdmin)

admin.site.register(SnippetsSet, SnippetsSetAdmin)
admin.site.register(XrumerBaseRaw, XrumerBaseRawAdmin)
admin.site.register(XrumerBaseR, XrumerBaseRAdmin)
admin.site.register(SpamTask, SpamTaskAdmin)
