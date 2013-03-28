#coding:utf-8
from django.conf.urls import patterns, include, url
from views import *
from cart.views import *

urlpatterns = patterns('',
    (r'^itemmore\/$',ajaxLineItem),
    (r'^itemattr\/(?P<t>\d{1})(?P<i>\d+)\/$',ajaxItemAttr),
    (r'^buy\/(?P<t>\d{1})(?P<i>\d+)\/$', ajaxCartItem,  {'f': buyToCart}),
    (r'^clear\/(?P<t>\d{1})(?P<i>\d+)\/$', ajaxCartItem,  {'f': clearCartItem}),
    (r'^itemnum\/(?P<t>\d+)\/(?P<i>\d+)\/$', ajaxCartItemNum,  {'f': changeCartItem}),
)