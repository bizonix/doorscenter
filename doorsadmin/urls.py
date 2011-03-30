from django.conf.urls.defaults import patterns
from doorsadmin.feeds import EventFeedError, EventFeedWarning

urlpatterns = patterns('',
    (r'^agents/(?P<agentId>\d+)/get$', 'doorsadmin.views.get'),
    (r'^agents/(?P<agentId>\d+)/update$', 'doorsadmin.views.update'),
    (r'^feeds/error$', EventFeedError()),
    (r'^feeds/warning$', EventFeedWarning()),
)
