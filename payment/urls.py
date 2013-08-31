#coding:utf-8
from new31.func import pPatterns
from views import pays

urlpatterns = pPatterns(
    (r'^$', pays, 3)
)