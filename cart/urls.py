#coding:utf-8
from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    (r'^$', cart),
    (r'^buy\/(?P<t>\d{1})(?P<i>\d+)\/$', hCart, {'f': toCart}),
    (r'^clear\/(?P<t>\d{1})(?P<i>\d+)\/$', hCart, {'f': clearCartItem}),
    (r'^consignee\/$', consignee),
)