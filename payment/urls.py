# coding: UTF-8
from new31.func import pPatterns
from views import pays, editPay, subEdit
from models import Pay

try:
    urls = []
    for i in Pay.objects.filter(onl=True):
        for ii in i.main.urls:
            urls.append((r'^api\/%s\/%s$' %  (i.cod, ii[0].lstrip('^').rstrip('$')), ii[1], 2))

    urls = tuple(urls)

except Exception, e:
    # raise e
    urls = ()

urlpatterns = pPatterns(
    (r'^$', pays, 3),
    (r'^edit\/(?P<id>\d+)\/$', editPay, 3),
    (r'^subedit\/$', subEdit, 3),
    *urls
)