#coding:utf-8
from django.conf.urls import patterns
from views import ordList, submit, addItem, delItem, newOrdUI, editUI, cCons

urlpatterns = patterns('',
    (r'^$', ordList),
    (r'^submit/$', submit),
    (r'^additem/$', addItem),
    (r'^delitem\/$', delItem),
    (r'^new/$',  newOrdUI),
    (r'^edit/$',  editUI),
    (r'^(?P<s>\d+)/$', cCons),
)