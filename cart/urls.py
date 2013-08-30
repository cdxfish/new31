#coding:utf-8
from new31.func import pPatterns
from views import cart, cnsgn, buy, delete, checkout, submit

urlpatterns = pPatterns(
    (r'^$', cart, 'cart', 2),
    (r'^consignee\/$', cnsgn, 'cnsgn', 2),
    (r'^buy\/$', buy, 'buy', 2),
    (r'^del\/$', delete, 'delete', 2),
    (r'^checkout\/$', checkout, 'checkInCart', 2),
    (r'^submit\/$', submit, 'subInCart', 2)
)