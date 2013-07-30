#coding:utf-8
from django.conf.urls import patterns, include, url
from views import iUI, iList, cOnl

urlpatterns = patterns('',
    (r'^$', iUI),
    (r'^list\/$', iList),
    (r'^conl\/$', cOnl),
)