from django.contrib import admin
from doorsadmin.models import *

class BaseAdmin(admin.ModelAdmin):
    list_per_page = 20

class BaseAdminManaged(BaseAdmin):
    actions = ['MakeStateManagedNew', 'MakeStateManagedDone']
    def MakeStateManagedNew(self, request, queryset):
        rows_updated = queryset.update(stateManaged='new')
        if rows_updated == 1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % rows_updated
        self.message_user(request, "%s successfully marked as new." % message_bit)
    MakeStateManagedNew.short_description = "1. Mark selected items as new"
    def MakeStateManagedDone(self, request, queryset):
        rows_updated = queryset.update(stateManaged='done')
        if rows_updated == 1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % rows_updated
        self.message_user(request, "%s successfully marked as done." % message_bit)
    MakeStateManagedDone.short_description = "2. Mark selected items as done"

'''Agents'''

class AgentAdmin(BaseAdmin):
    list_display = ('pk', 'type', 'description', 'currentTask', 'dateLastPing', 'interval', 'active', 'dateAdded')
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

class DomainAdmin(BaseAdmin):
    list_display = ('pk', 'name', 'niche', 'host', 'dateRegistered', 'dateExpires', 'maxDoorsCount', 'GetDoorsCount', 'GetPagesCount', 'active', 'stateSimple', 'dateAdded')
    list_filter = ['niche', 'dateExpires']
    fieldsets = [
        (None, {'fields': ['name', ('niche', 'host'), ('dateRegistered', 'dateExpires'), ('ipAddress', 'nameServer1', 'nameServer2'), 'maxDoorsCount', 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']
    
class HostAdmin(BaseAdmin):
    list_display = ('pk', 'type', 'company', 'hostName', 'costPerMonth', 'diskSpace', 'traffic', 'controlPanelType', 'GetIPAddressesCount', 'GetDomainsCount', 'GetDoorsCount', 'GetPagesCount', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['type', ('company', 'hostName'), ('costPerMonth', 'diskSpace', 'traffic'), ('controlPanelType', 'controlPanelUrl')]}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('FTP Account', {'fields': [('ftpLogin', 'ftpPassword', 'ftpPort'), 'rootDocumentTemplate'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class IPAddressAdmin(BaseAdmin):
    list_display = ('pk', 'address', 'host', 'GetDomainsCount', 'GetDoorsCount', 'GetPagesCount', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['address', 'host']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

'''Doorways group'''
    
class DoorwayAdmin(BaseAdminManaged):
    list_display = ('pk', 'net', 'niche', 'template', 'keywordsSet', 'pagesCount', 'GetDomainAndUrl', 'spamLinksCount', 'GetSpamTasksCount', 'GetRunTime', 'stateManaged', 'agent', 'dateAdded')
    list_filter = ['niche', 'net', 'stateManaged']
    fieldsets = [
        (None, {'fields': [('net', 'niche'), ('template', 'keywordsSet', 'pagesCount'), ('domain', 'domainFolder'), ('doorgenProfile', 'spamLinksCount'), 'doorwaySchedule']}),
        ('Lists', {'fields': ['keywordsList', 'netLinksList', 'spamLinksList'], 'classes': ['collapse']}),
        ('Analytics', {'fields': [('analyticsId', 'piwikId', 'cyclikId')], 'classes': ['collapse']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['doorwaySchedule', 'lastError', 'dateAdded', 'dateChanged']

class NicheAdmin(BaseAdmin):
    list_display = ('pk', 'description', 'language', 'GetDomainsCount', 'GetDoorsCount', 'GetPagesCount', 'GetKeywordsSetsCount', 'GetTemplatesCount', 'GetXrumerBasesRCount', 'GetSpamTasksCount', 'GetSnippetsSetsCount', 'active', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['description', 'language', 'active']}),
        ('Lists', {'fields': ['stopwordsList'], 'classes': ['collapse']}),
        ('Analytics', {'fields': [('analyticsId', 'piwikId', 'cyclikId')], 'classes': ['collapse']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class KeywordsSetAdmin(BaseAdmin):
    list_display = ('pk', 'description', 'niche', 'localFolder', 'encoding', 'keywordsCount', 'GetDoorsCount', 'GetPagesCount', 'active', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['description', 'niche', ('localFolder', 'encoding'), 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class TemplateAdmin(BaseAdmin):
    list_display = ('pk', 'description', 'niche', 'type', 'localFolder', 'GetDoorsCount', 'GetPagesCount', 'active', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['description', ('niche', 'type'), 'localFolder', 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class NetAdmin(BaseAdmin):
    list_display = ('pk', 'description', 'GetDoorsCount', 'GetPagesCount', 'active', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['description', 'netLinksList', 'active']}),
        ('Analytics', {'fields': [('analyticsId', 'piwikId', 'cyclikId')], 'classes': ['collapse']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class DoorgenProfileAdmin(BaseAdmin):
    list_display = ('pk', 'description', 'GetDoorsCount', 'GetPagesCount', 'active', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['description', 'settings', 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class DoorwayScheduleAdmin(BaseAdmin):
    list_display = ('pk', 'net', 'niche', 'template', 'keywordsSet', 'minPagesCount', 'maxPagesCount', 'minSpamLinksPercent', 'maxSpamLinksPercent', 'dateStart', 'dateEnd', 'doorsPerDay', 'GetDoorsCount', 'GetPagesCount', 'active', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': [('net', 'niche'), ('template', 'keywordsSet'), ('minPagesCount', 'maxPagesCount', 'minSpamLinksPercent', 'maxSpamLinksPercent'), ('dateStart', 'dateEnd', 'doorsPerDay'), 'active']}),
        ('Run', {'fields': [('lastRun', 'doorsThisDay')], 'classes': ['expand']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastRun', 'doorsThisDay', 'lastError', 'dateAdded', 'dateChanged']

'''Spam group'''

class XrumerProjectInline(admin.TabularInline):
    model = XrumerProject
    fields = ['xrumerBaseR', 'spamTask', 'localFile']
    
class SpamTaskAdmin(BaseAdminManaged):
    list_display = ('pk', 'niche', 'xrumerBaseR', 'GetDoorsCount', 'GetRunTime', 'stateManaged', 'agent', 'dateAdded')
    list_filter = ['niche', 'stateManaged']
    fieldsets = [
        (None, {'fields': ['niche', 'xrumerBaseR']}),
        ('Lists', {'fields': ['spamText', 'spamLinksList', 'doorways'], 'classes': ['collapse']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']
    inlines = [XrumerProjectInline]

class XrumerBaseRawAdmin(BaseAdminManaged):
    list_display = ('pk', 'baseNumber', 'GetXrumerBasesRCount', 'active', 'GetRunTime', 'stateManaged', 'agent', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['baseNumber', 'localFile', 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class XrumerBaseRAdmin(BaseAdmin):
    list_display = ('pk', 'baseNumber', 'niche', 'xrumerBaseRaw', 'GetSpamTasksCount', 'active', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['baseNumber', ('niche', 'xrumerBaseRaw'), 'localFile', 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']
    inlines = [XrumerProjectInline]

class XrumerProjectAdmin(BaseAdmin):
    list_display = ('pk', 'xrumerBaseR', 'spamTask', 'stateSimple', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['xrumerBaseR', 'spamTask', 'localFile']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']
    inlines = [XrumerProjectInline]

class SnippetsSetAdmin(BaseAdminManaged):
    list_display = ('pk', 'niche', 'localFile', 'keywordsCount', 'interval', 'dateLastParsed', 'phrasesCount', 'active', 'GetRunTime', 'stateManaged', 'agent', 'dateAdded')
    fieldsets = [
        (None, {'fields': ['niche', ('localFile', 'keywordsCount'), ('interval', 'dateLastParsed'), 'active']}),
        ('Lists', {'fields': ['phrasesList'], 'classes': ['collapse']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['dateLastParsed', 'lastError', 'dateAdded', 'dateChanged']

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

admin.site.register(SpamTask, SpamTaskAdmin)
admin.site.register(XrumerBaseRaw, XrumerBaseRawAdmin)
admin.site.register(XrumerBaseR, XrumerBaseRAdmin)
admin.site.register(XrumerProject, XrumerProjectAdmin)
admin.site.register(SnippetsSet, SnippetsSetAdmin)
