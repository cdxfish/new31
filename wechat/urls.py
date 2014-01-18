#coding:utf-8
from new31.func import pPatterns
from views import responseMsg, wechatShowTag, checkSignature, queryOrd

urlpatterns = pPatterns(
    (r'^$', responseMsg, 2),
    (r'^query\/$', queryOrd, 2),
    (r'^(?P<tag>.*)\/$', wechatShowTag, 2),
    (r'^signature\/$', checkSignature, 2)
)