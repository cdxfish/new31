#coding:utf-8
from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    (r'^$', cart),
    (r'^buy\/(?P<i>\d+)\/$', buy),
    (r'^consignee\/$', consignee),
)
