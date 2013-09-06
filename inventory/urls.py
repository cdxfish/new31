#coding:utf-8
from new31.func import pPatterns
from views import inventory, stockInv, cOnlInv, defaultInv, minusInv, plusInv

urlpatterns = pPatterns(
    (r'^$', inventory, 3),
    (r'^list\/$', stockInv, 3),
    (r'^conl\/(?P<sn>\d+)\/$', cOnlInv, 3),
    (r'^default\/(?P<s>\d{4}-\d{2}-\d{2})\/$', defaultInv, 3),
    (r'^minus\/(?P<sn>\d+)\/(?P<num>\d+)\/$', minusInv, 3),
    (r'^plus\/(?P<sn>\d+)\/(?P<num>\d+)\/$', plusInv, 3)
)