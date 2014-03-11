#coding:utf-8
from new31.func import pPatterns
from views import responseMsg, wechatShowTag, checkSignature, queryOrd
from tag.views import randomShow, tagShow

urlpatterns = pPatterns(
    (r'^$', responseMsg, 2),
    (r'^query\/$', queryOrd, 2),
    (r'^tag\/$', randomShow, 2),
    (r'^tag\/(?P<tag>.*)\/$', tagShow, 2),
    (r'^signature\/$', checkSignature, 2)
)