#coding:utf-8
from new31.func import pPatterns
from views import message

urlpatterns = pPatterns(
    (r'^$', message, 3)
)