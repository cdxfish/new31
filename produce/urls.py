#coding:utf-8
from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    (r'^$', produceUI),
    (r'^(?P<c>\d+)/$', pCon),
)