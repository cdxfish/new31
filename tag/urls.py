#coding:utf-8
from django.conf.urls import patterns, include, url
from views import *
from purview.views import *

urlpatterns = patterns('',
    (r'^tag\/$', Purview().check,{'appName':tagAdmin}),
    (r'^$',tag),
    (r'^(?P<tagTitle>.*)\/$',tag),
)