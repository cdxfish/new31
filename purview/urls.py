#coding:utf-8
from new31.func import pPatterns
from views import purview

urlpatterns = pPatterns(
    (r'^$', purview, 'purview', 3)
)