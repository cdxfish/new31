#coding:utf-8
from django.conf.urls import patterns, url, include
from django.conf import settings
from new31.func import Patterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    (r'^(nn\/$|cs\/$|km\/$|^$)', include('%s.urls' % settings.APPS.keys()[0])),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += Patterns(settings.APPS.keys()[1:])

if settings.DEBUG:
    urlpatterns += patterns('', 
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        
    )