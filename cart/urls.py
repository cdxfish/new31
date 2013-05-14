#coding:utf-8
from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    (r'^$', cart),
    (r'^buy\/(?P<specID>\d+)\/$', hFunc, {'func': buy}),
    (r'^clear\/(?P<specID>\d+)\/$', hFunc, {'func': clear}),
    (r'^itemnum\/(?P<num>\d+)\/(?P<specID>\d+)\/$', hFunc, {'func': changnum}),
    (r'^checkout\/$', checkout),
)