from django.contrib import admin
from doorsadmin.models import *
from django.contrib.admin.actions import delete_selected
delete_selected.short_description = '9. Delete selected items'

class BaseAdmin(admin.ModelAdmin):
    list_per_page = 20

def GetMessageBit(rows_updated):
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
    actions = ['MakeStateManagedNew', 'MakeStateManagedDone']
    def MakeStateManagedNew(self, request, queryset):
        rows_updated = queryset.update(stateManaged='new')
        self.message_user(request, "%s successfully marked as new." % GetMessageBit(rows_updated))
    MakeStateManagedNew.short_description = "3. Mark selected items as new"
    def MakeStateManagedDone(self, request, queryset):
        rows_updated = queryset.update(stateManaged='done')
        self.message_user(request, "%s successfully marked as done." % GetMessageBit(rows_updated))
    MakeStateManagedDone.short_description = "4. Mark selected items as done"

class BaseAdminSimple(BaseAdmin):
    actions = ['MakeStateSimpleOk']
    def MakeStateSimpleOk(self, request, queryset):
        rows_updated = queryset.update(stateSimple='ok')
        self.message_user(request, "%s successfully marked as ok." % GetMessageBit(rows_updated))
    MakeStateSimpleOk.short_description = "3. Mark selected items as ok"

'''Agents'''

class AgentAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'type', 'description', 'currentTask', 'GetDateLastPingAgo', 'interval', 'active', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['type', 'description', ('currentTask', 'dateLastPing', 'interval'), 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['currentTask', 'dateLastPing', 'lastError', 'dateAdded', 'dateChanged']

class EventAdmin(BaseAdmin):
    list_display = ('pk', 'date', 'type', 'object', 'text')
    fieldsets = [
        (None, {'fields': ['date', ('type', 'object'), 'text']}),
    ]
    readonly_fields = ['date', 'type', 'object', 'text']

'''Domains group'''

class DomainAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'name', 'niche', 'host', 'dateRegistered', 'dateExpires', 'GetDoorsMaxCount', 'GetPagesCount', 'active', 'stateSimple', 'dateAdded')
    list_filter = ['niche', 'dateExpires']
    fieldsets = [
        (None, {'fields': ['name', ('niche', 'host'), ('dateRegistered', 'dateExpires'), ('ipAddress', 'nameServer1', 'nameServer2'), 'maxDoorsCount', 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']
    
class HostAdmin(BaseAdminSimple):
    list_display = ('pk', 'type', 'company', 'hostName', 'costPerMonth', 'diskSpace', 'traffic', 'controlPanelType', 'GetIPAddressesCount', 'GetDomainsCount', 'GetDoorsCount', 'GetPagesCount', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['type', ('company', 'hostName'), ('costPerMonth', 'diskSpace', 'traffic'), ('controlPanelType', 'controlPanelUrl')]}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('FTP Account', {'fields': [('ftpLogin', 'ftpPassword', 'ftpPort'), 'rootDocumentTemplate'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class IPAddressAdmin(BaseAdminSimple):
    list_display = ('pk', 'address', 'host', 'GetDomainsCount', 'GetDoorsCount', 'GetPagesCount', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['address', 'host']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

'''Doorways group'''
    
class DoorwayAdmin(BaseAdminManaged):
    list_display = ('pk', 'niche', 'net', 'keywordsSet', 'template', 'doorgenProfile', 'pagesCount', 'spamLinksCount', 'GetUrl', 'GetSpamTasksCount', 'GetRunTime', 'stateManaged', 'agent', 'dateAdded')
    list_filter = ['niche', 'net', 'stateManaged']
    fieldsets = [
        (None, {'fields': [('niche', 'net'), ('keywordsSet', 'template', 'doorgenProfile'), ('domain', 'domainFolder'), ('pagesCount', 'spamLinksCount'), 'doorwaySchedule']}),
        ('Lists', {'fields': ['keywordsList', 'netLinksList', 'spamLinksList'], 'classes': ['collapse']}),
        ('Analytics', {'fields': [('analyticsId', 'piwikId', 'cyclikId')], 'classes': ['collapse']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['doorwaySchedule', 'lastError', 'dateAdded', 'dateChanged']

class NicheAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'description', 'language', 'GetDomainsCount', 'GetDoorsCount', 'GetPagesCount', 'GetKeywordsSetsCount', 'GetTemplatesCount', 'GetSnippetsSetsCount', 'GetXrumerBasesRCount', 'GetSpamTasksCount', 'active', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['description', 'language', 'active']}),
        ('Lists', {'fields': ['stopwordsList'], 'classes': ['collapse']}),
        ('Analytics', {'fields': [('analyticsId', 'piwikId', 'cyclikId')], 'classes': ['collapse']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class KeywordsSetAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'description', 'niche', 'localFolder', 'encoding', 'keywordsCount', 'GetDoorsCount', 'GetPagesCount', 'active', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['description', 'niche', ('localFolder', 'encoding'), 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class TemplateAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'description', 'niche', 'type', 'localFolder', 'GetDoorsCount', 'GetPagesCount', 'active', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['description', ('niche', 'type'), 'localFolder', 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class NetAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'description', 'GetDoorsCount', 'GetPagesCount', 'active', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['description', 'netLinksList', 'active']}),
        ('Analytics', {'fields': [('analyticsId', 'piwikId', 'cyclikId')], 'classes': ['collapse']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class DoorgenProfileAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'description', 'GetDoorsCount', 'GetPagesCount', 'active', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['description', 'settings', 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class DoorwayScheduleAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'niche', 'net', 'keywordsSet', 'template', 'doorgenProfile', 'dateStart', 'dateEnd', 'GetDoorsTodayCount', 'GetDoorsCount', 'GetPagesCount', 'active', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': [('niche', 'net'), ('keywordsSet', 'template', 'doorgenProfile'), ('minPagesCount', 'maxPagesCount', 'minSpamLinksPercent', 'maxSpamLinksPercent'), ('dateStart', 'dateEnd', 'doorsPerDay'), 'active']}),
        ('Run', {'fields': [('lastRun', 'doorsToday')], 'classes': ['expand']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastRun', 'doorsToday', 'lastError', 'dateAdded', 'dateChanged']

'''Spam group'''

class SpamTaskAdmin(BaseAdminManaged):
    list_display = ('pk', 'xrumerBaseR', 'snippetsSet', 'GetDoorsCount', 'successCount', 'halfSuccessCount', 'failsCount', 'profilesCount', 'GetRunTime', 'stateManaged', 'agent', 'dateAdded')
    list_filter = ['stateManaged']
    fieldsets = [
        (None, {'fields': [('xrumerBaseR', 'snippetsSet'), ('successCount', 'halfSuccessCount', 'failsCount', 'profilesCount')]}),
        ('Lists', {'fields': ['spamLinksList', 'doorways'], 'classes': ['collapse']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['successCount', 'halfSuccessCount', 'failsCount', 'profilesCount', 'lastError', 'dateAdded', 'dateChanged']

class SnippetsSetAdmin(BaseAdminActivatable, BaseAdminManaged):
    list_display = ('pk', 'niche', 'localFile', 'keywordsCount', 'interval', 'GetDateLastParsedAgo', 'phrasesCount', 'active', 'GetRunTime', 'stateManaged', 'agent', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['niche', ('localFile', 'keywordsCount'), ('interval', 'dateLastParsed'), 'active']}),
        ('Lists', {'fields': ['phrasesList'], 'classes': ['collapse']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['dateLastParsed', 'lastError', 'dateAdded', 'dateChanged']

class XrumerBaseRawAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'description', 'baseNumber', 'linksCount', 'GetXrumerBasesRCount', 'active', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['description', ('baseNumber', 'linksCount'), 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['linksCount', 'lastError', 'dateAdded', 'dateChanged']

class XrumerBaseRAdmin(BaseAdminActivatable, BaseAdminManaged):
    list_display = ('pk', 'description', 'baseNumber', 'linksCount', 'niche', 'xrumerBaseRaw', 'snippetsSet', 'GetSpamTasksCount', 'successCount', 'halfSuccessCount', 'failsCount', 'profilesCount', 'active', 'GetRunTime', 'stateManaged', 'agent', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['description', ('baseNumber', 'linksCount'), ('niche', 'xrumerBaseRaw', 'snippetsSet'), ('nickName', 'realName', 'password'), ('emailAddress', 'emailPopServer'), ('emailLogin', 'emailPassword'), 'subject', ('successCount', 'halfSuccessCount', 'failsCount', 'profilesCount'), 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['linksCount', 'nickName', 'realName', 'password', 'successCount', 'halfSuccessCount', 'failsCount', 'profilesCount', 'lastError', 'dateAdded', 'dateChanged']

admin.site.register(Agent, AgentAdmin)
admin.site.register(Event, EventAdmin)

admin.site.register(Domain, DomainAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(IPAddress, IPAddressAdmin)

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
