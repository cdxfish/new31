#coding:utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from views import *
from purview.views import *

urlpatterns = patterns('',
    (r'^$', Purview().check,{'appName': payList}),
)