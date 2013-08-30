#coding:utf-8
from new31.func import pPatterns
from views import deliver

urlpatterns = pPatterns(
    (r'^$', deliver, 'deliver', 3)
)