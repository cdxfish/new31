#coding:utf-8
from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    (r'^$', cart),
    (r'^buy\/(?P<specID>\d+)\/$', buy),
    (r'^clear\/(?P<mark>\d+)\/$', clear),
    (r'^checkout\/$', checkout),
)