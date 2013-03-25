#coding:utf-8
from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    (r'^moreitem\/$',ajaxLineItem),
    (r'^buy\/(?P<i>\d+)\/$',ajaxItemBuy),
    (r'^itemattr\/(?P<t>\d{1})(?P<i>\d+)\/$',ajaxItemAttr),
)