#coding:utf-8
from django.conf.urls import patterns, include, url
from views import login, logout, settings, saveSet, changepwd, cPwd, myOrd, viewOrd

urlpatterns = patterns('',
    (r'^$', myOrd),
    (r'^login\/$', login),
    (r'^logout\/$', logout),
    (r'^settings\/$', settings),
    (r'^sset\/$', saveSet),
    (r'^changepwd\/$', changepwd),
    (r'^cpwd\/$', cPwd),
    (r'^myord\/$', myOrd),
    (r'^view\/$', viewOrd),
)
