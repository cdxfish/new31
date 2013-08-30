#coding:utf-8
from new31.func import pPatterns
from views import ords, newOrdFrm, editOrdFrm, submitOrd, copyOrd, editOrd, confirmOrd, nullOrd, stopOrd, addItemOrd, delItemOrd

urlpatterns = pPatterns(
    (r'^$', ords, 'ords', 3),
    (r'^new/$',  newOrdFrm, 'newOrdFrm', 3),
    (r'^edit/$',  editOrdFrm, 'editOrdFrm', 3),
    (r'^submit\/$', submitOrd, 'submitOrd', 3),
    (r'^0\/$', copyOrd, 'copyOrd', 3),
    (r'^1\/$', editOrd, 'editOrd', 3),
    (r'^2\/$', confirmOrd, 'confirmOrd', 3),
    (r'^3\/$', nullOrd, 'nullOrd', 3),
    (r'^4\/$', stopOrd, 'stopOrd', 3),
    (r'^additem\/$', addItemOrd, 'addItemOrd', 3),
    (r'^delitem\/$', delItemOrd, 'delItemOrd', 3),
)