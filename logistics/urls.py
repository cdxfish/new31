#coding:utf-8
from new31.func import pPatterns
from views import logcs, logcsView, logcsUnsent, logcsEdit, logcsShip, logcsRefused, logcsSign, logcsStop, logcsEditFrm, logcsSub

urlpatterns = pPatterns(
    (r'^$', logcs, 'logcs', 3),
    (r'^view/$', logcsView, 'logcsView', 3),
    (r'^edit/$', logcsEditFrm, 'logcsEditFrm', 3),
    (r'^submit/$', logcsSub, 'logcsSub', 3),
    (r'^0\/$', logcsUnsent, 'logcsUnsent', 3),
    (r'^1\/$', logcsEdit, 'logcsEdit', 3),
    (r'^2\/$', logcsShip, 'logcsShip', 3),
    (r'^3\/$', logcsRefused, 'logcsRefused', 3),
    (r'^4\/$', logcsSign, 'logcsSign', 3),
    (r'^5\/$', logcsStop, 'logcsStop', 3)
)