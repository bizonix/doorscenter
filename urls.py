from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('',
    (r'^doorsadmin/', include('doorsadmin.urls')),
    (r'^sapeadmin/', include('sapeadmin.urls')),
    (r'^admin/', include(admin.site.urls)),
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
