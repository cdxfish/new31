#coding:utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from views import *

urlpatterns = patterns('',
    (r'^$', ordList),
    (r'^submit/$', submit),
    (r'^additemtoorder/$', addItemToOrd),
    (r'^delitem\/(?P<mark>\d+)\/$', delItemToOrd),
    (r'^new/$',  newOrdUI),
    (r'^edit/$',  editUI),
    (r'^(?P<c>\d+)/$', cCons),
)