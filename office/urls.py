#coding:utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from views import *

urlpatterns = patterns('',
    (r'^$', checkLogin,{'defName':office}),
)

