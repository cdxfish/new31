#coding:utf-8
from new31.func import pPatterns
from views import about

urlpatterns = pPatterns(
    (r'^$', about, 2)
)