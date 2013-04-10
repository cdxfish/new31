#coding:utf-8
from django.conf.urls import patterns
from views import *

urlpatterns = patterns('',
    (r'^$', office),
)