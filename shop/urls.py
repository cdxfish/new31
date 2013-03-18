#coding:utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from common import *
from views import *
import os.path

urlpatterns = patterns('',
    (r'^$', shop),
)