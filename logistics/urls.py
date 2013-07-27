#coding:utf-8
from django.conf.urls import patterns, include, url
from views import logcsUI, lCons, editUI, logcsSub

urlpatterns = patterns('',
    (r'^$', logcsUI),
    (r'^(?P<s>\d+)/$', lCons),
    (r'^edit/$', editUI),
    (r'^submit/$', logcsSub),
)