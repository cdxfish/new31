#coding:utf-8
from new31.func import pPatterns
from views import inv, iList, cOnl, default, minus, plus

urlpatterns = pPatterns(
    (r'^$', inv, 'inventory', 3),
    (r'^list\/$', iList, 'invList', 3),
    (r'^conl\/$', cOnl, 'invCOnl', 3),
    (r'^default\/$', default, 'invDefault', 3),
    (r'^minus\/$', minus, 'invmMinus', 3),
    (r'^plus\/$', plus, 'invPlus', 3)
)