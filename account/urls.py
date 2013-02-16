from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    (r'^settings\/$', settings),
    (r'^changepwd\/$', changepwd),
    (r'^order\/$', orderList),
    (r'^order\/(\d+)$', orderDetail),
)
