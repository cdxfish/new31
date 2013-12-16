#coding:utf-8
from new31.func import pPatterns
from views import upload

urlpatterns = pPatterns(
    (r'^$', upload, 3)
)