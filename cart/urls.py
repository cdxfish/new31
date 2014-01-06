# coding: UTF-8
from new31.func import pPatterns
from views import cart, cnsgn, buy, delInCart, checkout, submit, cNum

urlpatterns = pPatterns(
    (r'^$', cart, 2),
    (r'^consignee\/$', cnsgn, 2),
    (r'^buy\/(?P<sid>\d+)\/$', buy, 2),
    (r'^del\/(?P<mark>\d+)\/$', delInCart, 2),
    (r'^checkout\/$', checkout, 2),
    (r'^submit\/$', submit, 2),
    (r'^cnum\/(?P<mark>\d+)\/(?P<num>\d+)\/$', cNum, 0)
)