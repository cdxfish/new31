#coding:utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from views import *

urlpatterns = patterns('',
    (r'^$', orderList),
    (r'^submit/$', orderSubmit, {'func': carSub}),
    (r'^add/$', orderSubmit, {'func': adminSub}),
    (r'^new/$', newOrEditOrderUI),
    (r'^additemtoorder/$', addItemToOrder),
    (r'^delitem\/(?P<mark>\d+)\/$', hFunc, {'func': delItemToOrder}),
    (r'^ccon/(?P<c>\d+)/$', cCon),
)