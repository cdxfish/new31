#coding:utf-8
from new31.func import pPatterns
from views import ords, viewOrd, newOrdFrm, editOrdFrm, submitOrd, copyOrd, editOrd, confirmOrd, nullOrd, stopOrd, addItemOrd, delItemOrd

urlpatterns = pPatterns(
    (r'^$', ords, 3),
    (r'^view\/(?P<sn>\d{15})\/$', viewOrd, 3),
    (r'^new/$',  newOrdFrm, 3),
    (r'^edit/$',  editOrdFrm, 3),
    (r'^submit\/$', submitOrd, 3),
    (r'^0\/(?P<sn>\d{15})\/$', copyOrd, 3),
    (r'^1\/(?P<sn>\d{15})\/$', editOrd, 3),
    (r'^2\/(?P<sn>\d{15})\/$', confirmOrd, 3),
    (r'^3\/(?P<sn>\d{15})\/$', nullOrd, 3),
    (r'^4\/(?P<sn>\d{15})\/$', stopOrd, 3),
    (r'^additem\/$', addItemOrd, 3),
    (r'^delitem\/(?P<mark>\d+)\/$', delItemOrd, 3),
)