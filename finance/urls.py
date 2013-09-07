#coding:utf-8
from new31.func import pPatterns
from views import fnc, unpaidFnc, paidFnc, closedFnc, checkedFnc, stopFnc, cFnc

urlpatterns = pPatterns(
    (r'^$', fnc, 3),
    (r'^0\/(?P<sn>\d{15})\/$', unpaidFnc, 3),
    (r'^1\/(?P<sn>\d{15})\/$', paidFnc, 3),
    (r'^2\/(?P<sn>\d{15})\/$', closedFnc, 3),
    (r'^3\/(?P<sn>\d{15})\/$', checkedFnc, 3),
    (r'^4\/(?P<sn>\d{15})\/$', stopFnc, 3),
	(r'^cfnc\/$', cFnc, 0)

)