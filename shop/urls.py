#coding:utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from views import *
import os.path

info = {
    'a': randBox(),
}


urlpatterns = patterns('',
    (r'^$', shop, info),
)

