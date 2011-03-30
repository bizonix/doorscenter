# coding=utf8
from django.contrib.syndication.views import Feed
from django.db.models import Q
from doorsadmin.models import Event

class EventFeedBase(Feed):
    title = "Doorsadmin Events"
    link = "http://searchpro.name/doorscenter/admin/"
    def items(self):
        return Event.objects.order_by('-date')[:10]
    def item_title(self, item):
        if item.object:
            return item.object
        else:
            return 'General item'
    def item_description(self, item):
        return item.text
    def item_link(self, item):
        return 'http://searchpro.name/doorscenter/admin/doorsadmin/event/%d' % item.pk
    def item_pubdate(self, item):
        return item.date

class EventFeedError(EventFeedBase):
    title = "Doorsadmin Error Events"
    def items(self):
        return Event.objects.filter(type='error').order_by('-date')[:20]

class EventFeedWarning(EventFeedBase):
    title = "Doorsadmin Warning Events"
    def items(self):
        return Event.objects.filter(Q(type='error') | Q(type='warning')).order_by('-date')[:30]
