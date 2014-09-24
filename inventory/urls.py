# coding: UTF-8
from new31.func import pPatterns
from views import inventory, stockInv, sBuild, cOnlInv, defaultInv, minusInv, plusInv

urlpatterns = pPatterns(
    (r'^$', inventory, 3),
    (r'^list\/$', stockInv, 3),
    (r'^sbuild\/$', sBuild, 1),
    (r'^conl\/(?P<sid>\d+)\/(?P<bid>\d+)\/$', cOnlInv, 1),
    (r'^default\/(?P<s>\d{4}-\d{2}-\d{2})\/$', defaultInv, 3),
    (r'^minus\/(?P<sid>\d+)\/(?P<num>\d+)\/$', minusInv, 1),
    (r'^plus\/(?P<sid>\d+)\/(?P<num>\d+)\/$', plusInv, 1)
)