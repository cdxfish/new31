#coding:utf-8
from django.conf.urls import patterns
from views import fncUI, fCons

urlpatterns = patterns('',
    (r'^$', fncUI),
    (r'^(?P<s>\d+)/$', fCons),
)