#coding:utf-8
from django.conf.urls import patterns, include, url
from views import getItemPin, getItemSpec, cNum, cLogcs, cOrd, cFnc, cAdv, cDman, cItem, getItemByKeyword

urlpatterns = patterns('',
    (r'^itemmore\/$',getItemPin),
    (r'^itemspec\/$',getItemSpec),  #获取规格
    (r'^cnum\/$', cNum),
    (r'^clogcs\/$', cLogcs),
    (r'^cord\/$', cOrd),
    (r'^cfnc\/$', cFnc),
    (r'^cadv\/$', cAdv),
    (r'^cdman\/$', cDman),
    (r'^citem\/$', cItem),
    (r'^item\/$', getItemByKeyword),
)