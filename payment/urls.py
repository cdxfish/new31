#coding:utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from views import *
from office.common import *

urlpatterns = patterns('',
    (r'^$', Purview().check,{'appName': payList}),
)