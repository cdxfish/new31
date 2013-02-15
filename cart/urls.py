from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    (r'^$', hello),
    url(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'cart/images/'}),
)
