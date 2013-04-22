#coding:utf-8
from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    (r'^$', cart),
    (r'^buy\/(?P<t>\d{1})(?P<i>\d+)\/$', hCart, {'f': buyToCart}),
    (r'^clear\/(?P<t>\d{1})(?P<i>\d+)\/$', hCart, {'f': clearCartItem}),
    (r'^itemnum\/(?P<t>\d+)\/(?P<i>\d+)\/$', hCart,  {'f': changeCartItem}),
    (r'^consignee\/$', consignee),
    (r'^checkout\/$', checkout),
    (r'^ccon\/$', cConsigneeByCart),
)