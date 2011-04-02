from django.conf.urls.defaults import patterns
from doorsadmin.feeds import EventFeedError, EventFeedWarning, DoorwayFeed

urlpatterns = patterns('',
    (r'^agents/(?P<agentId>\d+)/get$', 'doorsadmin.views.get'),
    (r'^agents/(?P<agentId>\d+)/update$', 'doorsadmin.views.update'),
    (r'^feeds/error$', EventFeedError()),
    (r'^feeds/warning$', EventFeedWarning()),
    (r'^feeds/doorway$', DoorwayFeed()),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/favicon.ico'}),
)
