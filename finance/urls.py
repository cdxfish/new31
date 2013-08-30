#coding:utf-8
from new31.func import pPatterns
from views import fnc, unpaidFnc, paidFnc, closedFnc, checkedFnc, stopFnc

urlpatterns = pPatterns(
    (r'^$', fnc, 'fnc', 3),
    (r'^0\/$', unpaidFnc, 'unpaidFnc', 3),
    (r'^1\/$', paidFnc, 'paidFnc', 3),
    (r'^2\/$', closedFnc, 'closedFnc', 3),
    (r'^3\/$', checkedFnc, 'checkedFnc', 3),
    (r'^4\/$', stopFnc, 'stopFnc', 3)
)