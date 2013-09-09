#coding:utf-8
from new31.func import pPatterns
from views import logcs, logcsView, baiduMap, logcsUnsent, logcsEdit, logcsShip, logcsRefused, logcsSign, logcsStop, logcsEditFrm, logcsSub, cDman, cAdv, cLogcs

urlpatterns = pPatterns(
    (r'^$', logcs, 3),
    (r'^view/$', logcsView, 3),
    (r'^map\/$', baiduMap, 3),
    (r'^edit/$', logcsEditFrm, 3),
    (r'^submit/$', logcsSub, 3),
    (r'^0\/(?P<sn>\d{15})\/$', logcsUnsent, 1),
    (r'^1\/(?P<sn>\d{15})\/$', logcsEdit, 3),
    (r'^2\/(?P<sn>\d{15})\/$', logcsShip, 1),
    (r'^3\/(?P<sn>\d{15})\/$', logcsRefused, 1),
    (r'^4\/(?P<sn>\d{15})\/$', logcsSign, 1),
    (r'^5\/(?P<sn>\d{15})\/$', logcsStop, 1),
    (r'^cdman\/$', cDman, 1),
    (r'^cadv\/$', cAdv, 1),
    (r'^clogcs\/$', cLogcs, 0)

)