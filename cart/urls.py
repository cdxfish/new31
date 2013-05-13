#coding:utf-8
from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    (r'^$', cart),
    (r'^buy\/(?P<specID>\d+)\/$', buy),
    # (r'^clear\/P(?P<id>\d+)\/$', clearCartItem),
    # (r'^itemnum\/P(?P<id>\d+)\/$', changeCartItemNum),
    (r'^checkout\/$', checkout),
)