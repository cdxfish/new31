#coding:utf-8
from django.conf.urls import patterns, include, url
from views import *
from office.common import *

urlpatterns = patterns('',
    (r'^$', Purview().check,{'appName':itemAdmin}),
    (r'^item\/$', Purview().check,{'appName':itemAdd}),
)

