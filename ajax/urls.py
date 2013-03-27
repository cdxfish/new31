#coding:utf-8
from django.conf.urls import patterns, include, url
from views import *
from cart.views import *

urlpatterns = patterns('',
    (r'^moreitem\/$',ajaxLineItem),
    (r'^buy\/(?P<t>\d{1})(?P<i>\d+)\/$', ajaxCartItem,  {'f': toCart}),
    (r'^clear\/(?P<t>\d{1})(?P<i>\d+)\/$', ajaxCartItem,  {'f': clearCartItem}),
    (r'^itemattr\/(?P<t>\d{1})(?P<i>\d+)\/$',ajaxItemAttr),
)