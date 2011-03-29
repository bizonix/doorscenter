# coding=utf8
from django.contrib.syndication.views import Feed
from doorsadmin.models import Event

class EventErrorFeed(Feed):
    title = "Doorsadmin Error Events"
    link = "http://searchpro.name/doorscenter/admin/"
    def items(self):
        return Event.objects.filter(type='error').order_by('-date')[:20]
    def item_title(self, item):
        if item.object:
            return item.object
        else:
            return 'General error'
    def item_description(self, item):
        return item.text
    def item_link(self, item):
        return 'http://searchpro.name/doorscenter/admin/doorsadmin/event/%d' % item.pk
    def item_pubdate(self, item):
        return item.date
