#coding:utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from settings import APPS
from shop.common import *
from account.views import UserInfo

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# common = {'title': Shop().title('桑心').title, 'user': UserInfo().returnInfo()}



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', include('%s.urls' % settings.APPS[0])),
    url(r'^(nn\/$|cs\/$|km\/$|^$)', include('%s.urls' % settings.APPS[0])),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%scss/' % settings.STATIC_ROOT}),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static/js/'}),
    url(r'^(?P<path>.*\.ico)$', 'django.views.static.serve', {'document_root': 'static/'}),
    url(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static/images/'}),
    url(r'^m/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%simages/' % settings.MEDIA_ROOT}),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


for i in settings.APPS[1:]:
  urlpatterns += patterns('',
      (r'^%s/' % i , include( '%s.urls' % i)),
  )
