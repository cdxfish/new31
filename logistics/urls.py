#coding:utf-8
from new31.func import pPatterns
from views import logcs, baiduMap, logcsView, logcsUnsent, logcsEdit, logcsShip, logcsRefused, logcsSign, logcsStop, logcsEditFrm, logcsSub

urlpatterns = pPatterns(
    (r'^$', logcs, 3),
    (r'^map\/$', baiduMap, 3),
    (r'^view/$', logcsView, 3),
    (r'^edit/$', logcsEditFrm, 3),
    (r'^submit/$', logcsSub, 3),
    (r'^0\/$', logcsUnsent, 3),
    (r'^1\/$', logcsEdit, 3),
    (r'^2\/$', logcsShip, 3),
    (r'^3\/$', logcsRefused, 3),
    (r'^4\/$', logcsSign, 3),
    (r'^5\/$', logcsStop, 3)
)