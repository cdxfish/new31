#coding:utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from common import *
from views import *

urlpatterns = patterns('',
    (r'^$', Purview().check, {'appName':office}),
)