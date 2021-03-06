# coding=utf8
from django.contrib import admin
from doorsadmin.models import *
from django.contrib.admin.actions import delete_selected
import google, yahoo
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

class BaseAdminManaged(BaseAdmin):
    actions = ['MakeStateManagedNew', 'MakeStateManagedDone', 'MakePriorityHigh', 'MakePriorityStd', 'MakePriorityZero']
    def MakeStateManagedNew(self, request, queryset):
        rows_updated = queryset.update(stateManaged='new')
        self.message_user(request, "%s marked as new." % GetMessageBit(rows_updated))
    MakeStateManagedNew.short_description = "3. Mark selected items as new"
    def MakeStateManagedDone(self, request, queryset):
        rows_updated = queryset.update(stateManaged='done')
        self.message_user(request, "%s marked as done." % GetMessageBit(rows_updated))
    MakeStateManagedDone.short_description = "4. Mark selected items as done"
    def MakePriorityHigh(self, request, queryset):
        rows_updated = queryset.update(priority='high')
        self.message_user(request, "%s marked as priority high." % GetMessageBit(rows_updated))
    MakePriorityHigh.short_description = "5. Mark selected items as priority high"
    def MakePriorityStd(self, request, queryset):
        rows_updated = queryset.update(priority='std')
        self.message_user(request, "%s marked as priority std." % GetMessageBit(rows_updated))
    MakePriorityStd.short_description = "6. Mark selected items as priority std"
    def MakePriorityZero(self, request, queryset):
        rows_updated = queryset.update(priority='zero')
        self.message_user(request, "%s marked as priority zero." % GetMessageBit(rows_updated))
    MakePriorityZero.short_description = "7. Mark selected items as priority zero"

class BaseAdminSimple(BaseAdmin):
    actions = ['MakeStateSimpleOk']
    def MakeStateSimpleOk(self, request, queryset):
        rows_updated = queryset.update(stateSimple='ok')
        self.message_user(request, "%s marked as ok." % GetMessageBit(rows_updated))
    MakeStateSimpleOk.short_description = "3. Mark selected items as ok"

'''Реальные классы'''

class NicheAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'description', 'GetStopWordsCount', 'redirect', 'tdsId', 'GetNetsCount', 'GetKeywordsSetsCount', 'GetTemplatesCount', 'GetSnippetsSetsCount', 'GetXrumerBasesSpamCount', 'GetDomainsCount', 'GetDoorsCount', 'GetPagesCount', 'GetTrafficLastDay', 'GetTrafficLastMonth', 'GetTrafficLastDayRelative', 'GetTrafficLastMonthRelative', 'active', 'stateSimple', 'dateAdded')
    list_filter = ['language', 'active', 'stateSimple']
    ordering = ['description']
    fieldsets = [
        (None, {'fields': ['description', 'language', 'stopwordsList', 'active']}),
        ('TDS', {'fields': [('tdsId', 'redirect', 'redirectType', 'redirectDelay')], 'classes': ['expanded']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']
    list_per_page = 100

class NetPlanAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'description', 'domainGroup', 'niche', 'template', 'redirect', 'tdsId', 'makeSpam', 'GetNetsCount', 'domainsPerDay', 'doorsPerDay', 'minDoorsCount', 'maxDoorsCount', 'minPagesCount', 'maxPagesCount', 'active', 'stateSimple', 'dateAdded')
    list_filter = ['niche', 'active', 'stateSimple']
    ordering = ['description']
    fieldsets = [
        (None, {'fields': [('description', 'domainGroup'), ('niche', 'keywordsSet', 'template'), ('minDoorsCount', 'maxDoorsCount', 'minPagesCount', 'maxPagesCount'), 'settings', ('active', 'makeSpam', 'generateNetsNow')]}),
        ('Schedule', {'fields': [('netsCount', 'dateStart', 'dateEnd', 'domainsPerDay', 'doorsPerDay')], 'classes': ['expanded']}),
        ('TDS', {'fields': [('tdsId', 'redirect', 'redirectType', 'redirectDelay')], 'classes': ['expanded']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']
    list_per_page = 100
    actions = ['GenerateNets']
    def GenerateNets(self, request, queryset):
        '''Генерируем одну сеть по плану сеток'''
        processed = 0
        for netPlan in queryset:
            processed += netPlan.GenerateNets(1)
        self.message_user(request, "%s generated." % GetMessageBit(processed))
    GenerateNets.short_description = "a. Generate a net"

class NetAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'description', 'domainGroup', 'niche', 'template', 'redirect', 'tdsId', 'makeSpam', 'GetDomainsCount', 'domainsPerDay', 'doorsPerDay', 'GetDoorsCount', 'GetPagesCount', 'GetIndexCount', 'GetTrafficLastDay', 'GetTrafficLastMonth', 'GetTrafficLastDayRelative', 'GetTrafficLastMonthRelative', 'active', 'stateSimple', 'dateAdded')
    list_filter = ['niche', 'active', 'stateSimple']
    ordering = ['description']
    search_fields = ['description']
    fieldsets = [
        (None, {'fields': [('description', 'domainGroup'), ('niche', 'keywordsSet', 'template'), ('minDoorsCount', 'maxDoorsCount', 'minPagesCount', 'maxPagesCount'), 'settings', ('active', 'makeSpam', 'addDomainsNow', 'generateDoorsNow')]}),
        ('Schedule', {'fields': [('dateStart', 'dateEnd', 'domainsPerDay', 'doorsPerDay')], 'classes': ['expanded']}),
        ('TDS', {'fields': [('tdsId', 'redirect', 'redirectType', 'redirectDelay')], 'classes': ['expanded']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']
    list_per_page = 100
    actions = ['AddDomains', 'AddDomainsAll', 'GenerateDoorways', 'UpdateSECount', 'UpdateIndexCount', 'UpdateBackLinksCount']
    def AddDomains(self, request, queryset):
        '''Добавляем в сеть один домен'''
        processed = 0
        for net in queryset:
            net.AddDomains(1)
            processed += 1
        self.message_user(request, "%s added." % GetMessageBit(processed))
    AddDomains.short_description = "a. Add a domain"
    def AddDomainsAll(self, request, queryset):
        '''Добавляем в сеть один домен'''
        processed = 0
        for net in queryset:
            net.AddDomains()
            processed += 1
        self.message_user(request, "%s processed." % GetMessageBit(processed))
    AddDomainsAll.short_description = "b. Build the net"
    def GenerateDoorways(self, request, queryset):
        '''Генерируем в сети один дорвей'''
        processed = 0
        for net in queryset:
            net.GenerateDoorways(1)
            processed += 1
        self.message_user(request, "%s generated." % GetMessageBit(processed))
    GenerateDoorways.short_description = "c. Generate a doorway"
    def UpdateSECount(self, request, queryset):
        '''Проверяем индекс в гугле'''
        processed = 0
        google.Initialize()
        yahoo.Initialize()
        for net in queryset:
            for domain in net.domain_set.all():
                domain.UpdateIndexCount()
                domain.UpdateBackLinksCount()
            processed += 1
        self.message_user(request, "%s checked." % GetMessageBit(processed))
    UpdateSECount.short_description = "d. Check index and back links"
    def UpdateIndexCount(self, request, queryset):
        '''Проверяем индекс в гугле'''
        processed = 0
        google.Initialize()
        for net in queryset:
            for domain in net.domain_set.all():
                domain.UpdateIndexCount()
            processed += 1
        self.message_user(request, "%s checked." % GetMessageBit(processed))
    UpdateIndexCount.short_description = "e. Check index"
    def UpdateBackLinksCount(self, request, queryset):
        '''Проверяем индекс в гугле'''
        processed = 0
        yahoo.Initialize()
        for net in queryset:
            for domain in net.domain_set.all():
                domain.UpdateBackLinksCount()
            processed += 1
        self.message_user(request, "%s checked." % GetMessageBit(processed))
    UpdateBackLinksCount.short_description = "f. Check backlinks"

class KeywordsSetAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'niche', 'GetLocalFolder', 'encoding', 'keywordsCount', 'GetDoorsCount', 'GetPagesCount', 'GetTrafficLastDay', 'GetTrafficLastMonth', 'GetTrafficLastDayRelative', 'GetTrafficLastMonthRelative', 'active', 'stateSimple', 'dateAdded')
    list_filter = ['niche', 'active', 'stateSimple']
    ordering = ['niche__description']
    fieldsets = [
        (None, {'fields': ['niche', ('localFolder', 'keywordsCount', 'encoding'), 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class TemplateAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'niche', 'type', 'agent', 'localFolder', 'GetDoorsCount', 'GetPagesCount', 'GetTrafficLastDay', 'GetTrafficLastMonth', 'GetTrafficLastDayRelative', 'GetTrafficLastMonthRelative', 'active', 'stateSimple', 'dateAdded')
    list_filter = ['niche', 'active', 'stateSimple']
    ordering = ['niche__description']
    fieldsets = [
        (None, {'fields': [('niche', 'type', 'agent'), 'localFolder', 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class SnippetsSetAdmin(BaseAdminActivatable, BaseAdminManaged):
    list_display = ('pk', 'niche', 'localFile', 'keywordsCount', 'interval', 'GetDateLastParsedAgo', 'phrasesCount', 'active', 'priority', 'GetRunTime', 'stateManaged', 'dateChanged', 'dateAdded')
    list_filter = ['niche', 'active', 'stateManaged', 'priority']
    ordering = ['niche__description']
    fieldsets = [
        (None, {'fields': ['niche', ('localFile', 'keywordsCount'), ('interval', 'dateLastParsed'), 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'agent', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['dateLastParsed', 'lastError', 'dateAdded', 'dateChanged']

class DomainAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'GetDomainUrl', 'group', 'host', 'niche', 'net', 'makeSpam', 'GetMaxDoorsCount', 'GetPagesCount', 'GetIndexCount', 'GetIndexCountDate', 'trafficLastDay', 'trafficLastMonth', 'GetAge', 'GetDateExpires', 'IsIndexed', 'active', 'stateSimple', 'dateAdded')
    list_filter = ['niche', 'net', 'host', 'group', 'banned', 'active', 'stateSimple']
    search_fields = ['name']
    fieldsets = [
        (None, {'fields': [('name', 'drop'), ('host', 'ipAddress'), ('niche', 'net', 'group', 'maxDoorsCount'), ('nameServer1', 'nameServer2', 'useOwnDNS', 'autoSubdomains'), ('dateRegistered', 'dateExpires', 'dateBan'), ('active', 'makeSpam')]}),
        ('Net properties', {'fields': [('linkedDomains')], 'classes': ['expanded']}),
        ('Bulk add domains', {'fields': [('bulkAddDomains')], 'classes': ['expanded']}),
        ('TDS', {'fields': [('tdsId', 'redirect', 'redirectType', 'redirectDelay')], 'classes': ['expanded']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['dateBan', 'lastError', 'dateAdded', 'dateChanged']
    actions = ['UpdateSECount', 'UpdateIndexCount', 'UpdateBackLinksCount', 'CheckOwnership', 'Reset', 'Prolongate', 'DeleteFromCP']
    def UpdateSECount(self, request, queryset):
        '''Проверяем индекс в гугле'''
        processed = 0
        google.Initialize()
        yahoo.Initialize()
        for domain in queryset:
            domain.UpdateIndexCount()
            domain.UpdateBackLinksCount()
            processed += 1
        self.message_user(request, "%s checked." % GetMessageBit(processed))
    UpdateSECount.short_description = "a. Check index and back links"
    def UpdateIndexCount(self, request, queryset):
        '''Проверяем индекс в гугле'''
        processed = 0
        google.Initialize()
        for domain in queryset:
            domain.UpdateIndexCount()
            processed += 1
        self.message_user(request, "%s checked." % GetMessageBit(processed))
    UpdateIndexCount.short_description = "b. Check index only"
    def UpdateBackLinksCount(self, request, queryset):
        '''Проверяем индекс в гугле'''
        processed = 0
        yahoo.Initialize()
        for domain in queryset:
            domain.UpdateBackLinksCount()
            processed += 1
        self.message_user(request, "%s checked." % GetMessageBit(processed))
    UpdateBackLinksCount.short_description = "c. Check back links only"
    def CheckOwnership(self, request, queryset):
        '''Проверка на то, что домен не отобрали'''
        processed = 0
        failed = 0
        for domain in queryset:
            if not domain.CheckOwnership():
                failed += 1
            processed += 1
        self.message_user(request, "%s checked, %d failed." % (GetMessageBit(processed), failed))
    CheckOwnership.short_description = "d. Check ownership"
    def Reset(self, request, queryset):
        '''Сбрасываем параметры доменов'''
        processed = 0
        for domain in queryset:
            domain.Reset()
            processed += 1
        self.message_user(request, "%s reset." % GetMessageBit(processed))
    Reset.short_description = "e. Reset domains"
    def Prolongate(self, request, queryset):
        '''Продляем регистрацию доменов'''
        processed = 0
        for domain in queryset:
            domain.Prolongate()
            processed += 1
        self.message_user(request, "%s prolongated." % GetMessageBit(processed))
    Prolongate.short_description = "f. Prolongate"
    def DeleteFromCP(self, request, queryset):
        '''Удаляем домены из панели управления'''
        processed = 0
        for domain in queryset:
            domain.DeleteFromCP()
            processed += 1
        self.message_user(request, "%s deleted from CP." % GetMessageBit(processed))
    DeleteFromCP.short_description = "g. Delete from CP"

class DoorwayAdmin(BaseAdminManaged):
    list_display = ('pk', 'niche', 'GetNet', 'template', 'keywordsSet', 'pagesCount', 'GetLinksCount', 'makeSpam', 'GetUrl', 'trafficLastDay', 'trafficLastMonth', 'priority', 'GetRunTime', 'stateManaged', 'dateChanged', 'dateAdded')
    list_filter = ['niche', 'domain__net', 'template', 'keywordsSet', 'stateManaged', 'priority']
    search_fields = ['domain__name']
    fieldsets = [
        (None, {'fields': [('niche'), ('keywordsSet', 'template'), ('domain', 'domainSub', 'domainFolder'), ('pagesCount', 'doorLinksCount', 'spamLinksCount', 'makeSpam')]}),
        ('Lists', {'fields': ['keywordsList', 'netLinksList'], 'classes': ['expanded']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'agent', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']
    #inlines = [DoorLinkInline]

class DoorLinkInline(admin.TabularInline):
    model = DoorLink
    extra = 1

class DoorLinkAdmin(BaseAdmin):
    list_display = ('pk', 'url', 'anchor', 'makeSpam', 'spamTask', 'GetSpamTaskState')
    search_fields = ['url', 'anchor']
    fieldsets = [
        (None, {'fields': [('url', 'anchor'), ('doorway', 'spamTask', 'makeSpam')]}),
    ]

class XrumerBaseSpamAdmin(BaseAdminActivatable, BaseAdminManaged):
    list_display = ('baseNumber', 'niche', 'linksCount', 'baseType', 'dateLastParsed', 'successCount', 'halfSuccessCount', 'failsCount', 'GetSpamTasksCount', 'active', 'priority', 'GetRunTime', 'stateManaged', 'dateChanged', 'dateAdded')
    list_filter = ['niche', 'active', 'stateManaged', 'priority']
    ordering = ['niche__description']
    fieldsets = [
        (None, {'fields': [('niche', 'linksCount', 'dateLastParsed'), ('baseNumber', 'xrumerBaseRaw', 'snippetsSet'), ('nickName', 'realName', 'password'), ('emailAddress'), ('baseType', 'creationType', 'registerRun', 'registerRunDate', 'registerRunTimeout'), ('successCount', 'halfSuccessCount', 'failsCount', 'profilesCount', 'registeredAccountsCount'), 'active']}),
        ('Spam parameters', {'fields': [('spamTaskDomainsMin', 'spamTaskDomainsMax', 'spamTaskDomainLinksMin', 'spamTaskDomainLinksMax')], 'classes': ['expanded']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'agent', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['registerRun', 'registerRunDate', 'successCount', 'halfSuccessCount', 'failsCount', 'profilesCount', 'registeredAccountsCount', 'lastError', 'dateAdded', 'dateChanged']
    actions = ['ResetNames', 'ResetNamesAndNew']
    def ResetNames(self, request, queryset):
        '''Сбрасываем имена'''
        processed = 0
        for base in queryset:
            base.ResetNames()
            processed += 1
        self.message_user(request, "%s reset." % GetMessageBit(processed))
    ResetNames.short_description = "a. Reset names"
    def ResetNamesAndNew(self, request, queryset):
        '''Сбрасываем имена и помечаем как новые'''
        processed = 0
        for base in queryset:
            base.stateManaged = 'new'
            base.ResetNames()
            processed += 1
        self.message_user(request, "%s reset and marked as new." % GetMessageBit(processed))
    ResetNamesAndNew.short_description = "3a. Reset names and mark as new"

class SpamTaskAdmin(BaseAdminManaged):
    list_display = ('pk', 'xrumerBaseSpam', 'GetSpamLinksCount', 'successCount', 'halfSuccessCount', 'failsCount', 'priority', 'GetRunTime', 'stateManaged', 'dateChanged', 'dateAdded')
    list_filter = ['stateManaged', 'priority']
    fieldsets = [
        (None, {'fields': [('xrumerBaseSpam'), ('successCount', 'halfSuccessCount', 'failsCount', 'profilesCount', 'registeredAccountsCount')]}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'agent', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['successCount', 'halfSuccessCount', 'failsCount', 'profilesCount', 'registeredAccountsCount', 'lastError', 'dateAdded', 'dateChanged']
    #inlines = [DoorLinkInline]

class SpamProfileTaskAdmin(BaseAdminManaged):
    list_display = ('pk', 'xrumerBaseRaw', 'homePage', 'profilesCount', 'registeredAccountsCount', 'successCount', 'halfSuccessCount', 'failsCount', 'priority', 'GetRunTime', 'stateManaged', 'dateChanged', 'dateAdded')
    list_filter = ['stateManaged', 'priority']
    search_fields = ['homePage', 'signature']
    fieldsets = [
        (None, {'fields': [('xrumerBaseRaw'), 'homePage', 'signature', ('profilesCount', 'registeredAccountsCount', 'successCount', 'halfSuccessCount', 'failsCount')]}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'agent', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['successCount', 'halfSuccessCount', 'failsCount', 'profilesCount', 'registeredAccountsCount', 'lastError', 'dateAdded', 'dateChanged']

class XrumerBaseDoorsAdmin(BaseAdminActivatable, BaseAdminManaged):
    list_display = ('baseNumber', 'niche', 'linksCount', 'xrumerBaseRaw', 'dateLastParsed', 'successCount', 'halfSuccessCount', 'failsCount', 'runCount', 'active', 'priority', 'GetRunTime', 'stateManaged', 'dateChanged', 'dateAdded')
    list_filter = ['niche', 'active', 'stateManaged', 'priority']
    ordering = ['niche__description']
    fieldsets = [
        (None, {'fields': [('niche', 'linksCount', 'dateLastParsed'), ('baseNumber', 'xrumerBaseRaw', 'snippetsSet'), ('nickName', 'realName', 'password'), ('emailAddress'), ('creationType', 'registerRun', 'registerRunDate', 'registerRunTimeout'), ('successCount', 'halfSuccessCount', 'failsCount', 'profilesCount', 'registeredAccountsCount'), 'active']}),
        ('Doorway parameters', {'fields': [('body'), ('runCount')], 'classes': ['expanded']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'agent', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['registerRun', 'registerRunDate', 'successCount', 'halfSuccessCount', 'failsCount', 'profilesCount', 'registeredAccountsCount', 'lastError', 'dateAdded', 'dateChanged']
    actions = ['ResetNames']
    def ResetNames(self, request, queryset):
        '''Сбрасываем имена'''
        processed = 0
        for base in queryset:
            base.ResetNames()
            processed += 1
        self.message_user(request, "%s reset." % GetMessageBit(processed))
    ResetNames.short_description = "a. Reset names"

class HostAdmin(BaseAdminSimple):
    list_display = ('pk', 'type', 'company', 'hostName', 'costPerMonth', 'diskSpace', 'traffic', 'controlPanelType', 'GetIPAddressesCount', 'GetDomainsCount', 'GetDoorsCount', 'GetPagesCount', 'GetTrafficLastDay', 'GetTrafficLastMonth', 'GetTrafficLastDayRelative', 'GetTrafficLastMonthRelative', 'stateSimple', 'dateAdded')
    list_filter = ['stateSimple']
    fieldsets = [
        (None, {'fields': ['type', ('company', 'hostName'), ('costPerMonth', 'diskSpace', 'traffic'), ('controlPanelType', 'controlPanelUrl', 'controlPanelServerId')]}),
        ('FTP Account', {'fields': [('ftpLogin', 'ftpPassword', 'ftpPort'), 'rootDocumentTemplate'], 'classes': ['expanded']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class IPAddressAdmin(BaseAdminSimple):
    list_display = ('pk', 'address', 'host', 'GetDomainsCount', 'GetDoorsCount', 'GetPagesCount', 'GetTrafficLastDay', 'GetTrafficLastMonth', 'GetTrafficLastDayRelative', 'GetTrafficLastMonthRelative', 'stateSimple', 'dateAdded')
    list_filter = ['stateSimple']
    ordering = ['address']
    fieldsets = [
        (None, {'fields': ['address', 'host']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

class XrumerBaseRawAdmin(BaseAdminActivatable, BaseAdminManaged):
    list_display = ('baseNumber', 'linksCount', 'successCount', 'halfSuccessCount', 'failsCount', 'profilesCount', 'registeredAccountsCount', 'GetXrumerBasesSpamCount', 'active', 'priority', 'GetRunTime', 'stateManaged', 'dateChanged', 'dateAdded')
    list_filter = ['active', 'stateManaged', 'priority']
    fieldsets = [
        (None, {'fields': [('niche', 'linksCount'), ('baseNumber', 'snippetsSet'), ('nickName', 'realName', 'password'), ('emailAddress'), ('successCount', 'halfSuccessCount', 'failsCount', 'profilesCount', 'registeredAccountsCount'), 'active']}),
        ('Parameters', {'fields': ['parseParams'], 'classes': ['expanded']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'agent', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['registerRun', 'registerRunDate', 'successCount', 'halfSuccessCount', 'failsCount', 'profilesCount', 'registeredAccountsCount', 'lastError', 'dateAdded', 'dateChanged']
    actions = ['ResetNames', 'ResetNamesAndNew']
    def ResetNames(self, request, queryset):
        '''Сбрасываем имена'''
        processed = 0
        for base in queryset:
            base.ResetNames()
            processed += 1
        self.message_user(request, "%s reset." % GetMessageBit(processed))
    ResetNames.short_description = "a. Reset names"
    def ResetNamesAndNew(self, request, queryset):
        '''Сбрасываем имена и помечаем как новые'''
        processed = 0
        for base in queryset:
            base.stateManaged = 'new'
            base.ResetNames()
            processed += 1
        self.message_user(request, "%s reset and marked as new." % GetMessageBit(processed))
    ResetNamesAndNew.short_description = "3a. Reset names and mark as new"

class AgentAdmin(BaseAdminSimple, BaseAdminActivatable):
    list_display = ('pk', 'type', 'description', 'host', 'ipAddress', 'currentTask', 'GetTasksState', 'GetDateLastPingAgo', 'interval', 'used', 'active', 'stateSimple', 'dateAdded')
    list_filter = ['used', 'active', 'stateSimple']
    fieldsets = [
        (None, {'fields': ['description', ('type', 'host', 'ipAddress'), 'params', ('currentTask', 'dateLastPing', 'interval', 'used'), 'active']}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateSimple', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['currentTask', 'dateLastPing', 'ipAddress', 'lastError', 'dateAdded', 'dateChanged']

class EventAdmin(BaseAdmin):
    list_display = ('pk', 'date', 'type', 'object', 'text')
    list_filter = ['type']
    search_fields = ['object', 'text']
    fieldsets = [
        (None, {'fields': ['date', ('type', 'object'), 'text']}),
    ]
    readonly_fields = ['date', 'type', 'object', 'text']

class ReportAdmin(BaseAdmin):
    list_display = ('pk', 'description', 'GetReport')
    ordering = ['description']
    fieldsets = [
        (None, {'fields': ['description', ('host', 'database'), ('user', 'password'), 'sql']}),
    ]

class RedirectTypeAdmin(BaseAdmin):
    list_display = ('pk', 'description', 'fileName')
    ordering = ['fileName']
    fieldsets = [
        (None, {'fields': ['description', 'fileName']}),
    ]

class TestQueueAdmin(BaseAdminManaged):
    list_display = ('pk', 'paramIn', 'paramOut', 'priority', 'GetRunTime', 'stateManaged', 'dateChanged', 'dateAdded')
    fieldsets = [
        (None, {'fields': [('paramIn', 'paramOut')]}),
        ('Remarks', {'fields': ['remarks'], 'classes': ['collapse']}),
        ('State information', {'fields': [('stateManaged', 'agent', 'lastError'), ('dateAdded', 'dateChanged')], 'classes': ['collapse']}),
    ]
    readonly_fields = ['lastError', 'dateAdded', 'dateChanged']

admin.site.register(Niche, NicheAdmin)
admin.site.register(NetPlan, NetPlanAdmin)
admin.site.register(Net, NetAdmin)
admin.site.register(KeywordsSet, KeywordsSetAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(SnippetsSet, SnippetsSetAdmin)

admin.site.register(Domain, DomainAdmin)
admin.site.register(Doorway, DoorwayAdmin)
admin.site.register(DoorLink, DoorLinkAdmin)
admin.site.register(XrumerBaseSpam, XrumerBaseSpamAdmin)
admin.site.register(SpamTask, SpamTaskAdmin)
admin.site.register(SpamProfileTask, SpamProfileTaskAdmin)
admin.site.register(XrumerBaseDoors, XrumerBaseDoorsAdmin)

admin.site.register(Host, HostAdmin)
admin.site.register(IPAddress, IPAddressAdmin)
admin.site.register(XrumerBaseRaw, XrumerBaseRawAdmin)

admin.site.register(Agent, AgentAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(RedirectType, RedirectTypeAdmin)

admin.site.register(TestQueue, TestQueueAdmin)
