#coding:utf-8
from django.conf.urls import patterns, url, include
from django.conf import settings
from account.views import UserInfo

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^(nn\/$|cs\/$|km\/$|^$)', include('%s.urls' % settings.APPS.keys()[0])),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


for i in settings.APPS.keys()[1:]:
  urlpatterns += patterns('',
      (r'^%s/' % i , include('%s.urls' % i)),
  )


if settings.DEBUG:
    urlpatterns += patterns('', 
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        
    )