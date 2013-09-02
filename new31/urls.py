#coding:utf-8
from django.conf.urls import patterns, url, include
from django.conf import settings
from new31.func import Patterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^(nn\/$|cs\/$|km\/$|^$)', 'shop.views.shop', name='shop'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin\/', include(admin.site.urls)),
)

urlpatterns += Patterns(settings.APPS.keys())

if settings.DEBUG:
    urlpatterns += patterns('', 
        url(r'^media\/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        
    )