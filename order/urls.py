#coding:utf-8
from new31.func import pPatterns
from views import ords, viewOrd, newOrdFrm, editOrdFrm, submitOrd, copyOrd, editOrd, confirmOrd, nullOrd, stopOrd, addItemOrd, delItemOrd

urlpatterns = pPatterns(
    (r'^$', ords, 3),
    (r'^view\/(?P<sn>\d{15})\/$', viewOrd, 3),
    (r'^new/$',  newOrdFrm, 3),
    (r'^edit/$',  editOrdFrm, 3),
    (r'^submit\/$', submitOrd, 3),
    (r'^0\/$', copyOrd, 3),
    (r'^1\/$', editOrd, 3),
    (r'^2\/$', confirmOrd, 3),
    (r'^3\/$', nullOrd, 3),
    (r'^4\/$', stopOrd, 3),
    (r'^additem\/$', addItemOrd, 3),
    (r'^delitem\/(?P<mark>\d+)\/$', delItemOrd, 3),
)