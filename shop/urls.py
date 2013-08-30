#coding:utf-8
from new31.func import pPatterns
from views import shop

urlpatterns = pPatterns(
    (r'^$', shop, 'shop', 2)
)