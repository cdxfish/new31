#coding:utf-8
from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    (r'^$', logisticsUI),
    (r'^ccon/(?P<c>\d+)/$', cCon),
)