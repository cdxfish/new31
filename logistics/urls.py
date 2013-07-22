#coding:utf-8
from django.conf.urls import patterns, include, url
from views import logcsUI, lCons, editUI, shipSub

urlpatterns = patterns('',
    (r'^$', logcsUI),
    (r'^(?P<c>\d+)/$', lCons),
    (r'^edit/$', editUI),
    (r'^submit/$', shipSub),
)