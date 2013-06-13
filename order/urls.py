#coding:utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from views import *

urlpatterns = patterns('',
    (r'^$', orderList),
    (r'^submit/$', carSub),
    (r'^add/$', adminSub),
    (r'^additemtoorder/$', addItemToOrder),
    (r'^delitem\/(?P<mark>\d+)\/$', delItemToOrder),
    (r'^new/$',  newOrEditOrderUI),
    (r'^ccon/(?P<c>\d+)/$', cCon),
)