# coding=utf8
from django.contrib import admin
from django.contrib.admin.actions import delete_selected
from blogsadmin.models import *
delete_selected.short_description = 'Delete'

class BlogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'domain', 'group', 'GetIndexCount', 'GetBackLinksCount', 'lastChecked')
    list_filter = ['group']
    search_fields = ['domain']
    ordering = ['domain']
    fieldsets = [
        (None, {'fields': [('domain', 'group')]}),
        ('Stats', {'fields': [('indexCount', 'backLinksCount', 'lastChecked')], 'classes': ['expanded']}),
        ('Bulk Actions', {'fields': ['bulkAddBlogs'], 'classes': ['expanded']}),
    ]
    readonly_fields = ['indexCount', 'backLinksCount', 'lastChecked']
    list_per_page = 100
    actions = ['Check']
    def Check(self, request, queryset):
        processed = 0
        for item in queryset:
            item.Check()
            processed += 1
        self.message_user(request, "%d blogs checked." % processed)
    Check.short_description = "1. Check"

class PositionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'blog', 'keyword', 'group', 'GetGooglePosition', 'googleMaxPosition', 'GetYahooPosition', 'yahooMaxPosition', 'GetBingPosition', 'bingMaxPosition', 'lastChecked')
    list_filter = ['group']
    search_fields = ['blog', 'keyword']
    ordering = ['blog', 'keyword']
    fieldsets = [
        (None, {'fields': ['blog', ('keyword', 'group')]}),
        ('Google', {'fields': [('googlePosition', 'googleMaxPosition', 'googleMaxPositionDate', 'googleExtendedInfo')], 'classes': ['expanded']}),
        ('Yahoo', {'fields': [('yahooPosition', 'yahooMaxPosition', 'yahooMaxPositionDate', 'yahooExtendedInfo')], 'classes': ['expanded']}),
        ('Bing', {'fields': [('bingPosition', 'bingMaxPosition', 'bingMaxPositionDate', 'bingExtendedInfo')], 'classes': ['expanded']}),
        ('Bulk Actions', {'fields': ['bulkAddKeywords'], 'classes': ['expanded']}),
    ]
    readonly_fields = ['googlePosition', 'googleMaxPosition', 'googleMaxPositionDate', 'googleExtendedInfo', 'yahooPosition', 'yahooMaxPosition', 'yahooMaxPositionDate', 'yahooExtendedInfo', 'bingPosition', 'bingMaxPosition', 'bingMaxPositionDate', 'bingExtendedInfo', 'lastChecked']
    list_per_page = 100
    actions = ['Check']
    def Check(self, request, queryset):
        processed = 0
        for item in queryset:
            item.Check()
            processed += 1
        self.message_user(request, "%d positions checked." % processed)
    Check.short_description = "1. Check"

admin.site.register(Blog, BlogAdmin)
admin.site.register(Position, PositionAdmin)
