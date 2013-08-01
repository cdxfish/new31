#coding:utf-8
from django.conf.urls import patterns, include, url
from views import login, logout, settings, changepwd, myOrd, viewOrd

urlpatterns = patterns('',
    (r'^login\/$', login),
    (r'^logout\/$', logout),
    (r'^settings\/$', settings),
    (r'^changepwd\/$', changepwd),
    (r'^myord\/$', myOrd),
    (r'^view\/$', viewOrd),
)
