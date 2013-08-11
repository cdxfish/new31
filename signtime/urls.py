#coding:utf-8
from django.conf.urls import patterns
from views import signtimeAdmin

urlpatterns = patterns('',
    (r'^$', signtimeAdmin),
)