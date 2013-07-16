#coding:utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from views import *

urlpatterns = patterns('',
    (r'^$', orderList),
    (r'^submit/$', submit),
    (r'^additemtoorder/$', addItemToOrder),
    (r'^delitem\/(?P<mark>\d+)\/$', delItemToOrder),
    (r'^new/$',  newOrderUI),
    (r'^(?P<c>\d+)/$', cCons),
)