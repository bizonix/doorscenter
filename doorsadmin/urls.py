from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^agents/(?P<agentId>\d+)/get$', 'doorsadmin.views.get'),
    (r'^agents/(?P<agentId>\d+)/update$', 'doorsadmin.views.update'),
    (r'^agents/(?P<agentId>\d+)/ping$', 'doorsadmin.views.ping'),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/favicon.ico'}),
)
