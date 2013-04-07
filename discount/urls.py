#coding:utf-8
from django.conf.urls import patterns, include, url
from views import *
from purview.views import *

urlpatterns = patterns('',
    (r'^admin\/$', Purview().check,{'appName':specAdmin}),
)