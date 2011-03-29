from django.conf.urls.defaults import *
from doorsadmin.models import *
from doorsadmin.feeds import *


urlpatterns = patterns('',
    (r'^agents/(?P<agentId>\d+)/get$', 'doorsadmin.views.get'),
    (r'^agents/(?P<agentId>\d+)/update$', 'doorsadmin.views.update'),
    (r'^feeds/error$', EventErrorFeed()),
)
