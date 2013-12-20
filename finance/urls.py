#coding:utf-8
from new31.func import pPatterns
from views import fnc, unpaidFnc, paidFnc, closedFnc, checkedFnc, stopFnc, reimburseFnc, cFnc

urlpatterns = pPatterns(
    (r'^$', fnc, 3),
    (r'^(?P<s>0)\/(?P<sn>\d{15})\/$', unpaidFnc, 3),
    (r'^(?P<s>1)\/(?P<sn>\d{15})\/$', paidFnc, 3),
    (r'^(?P<s>2)\/(?P<sn>\d{15})\/$', closedFnc, 3),
    (r'^(?P<s>3)\/(?P<sn>\d{15})\/$', checkedFnc, 3),
    (r'^(?P<s>4)\/(?P<sn>\d{15})\/$', stopFnc, 3),
    (r'^(?P<s>5)\/(?P<sn>\d{15})\/$', reimburseFnc, 3),
	(r'^cfnc\/$', cFnc, 0)

)