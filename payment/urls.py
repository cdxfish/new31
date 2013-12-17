#coding:utf-8
from new31.func import pPatterns
from views import pays, editPay, subEdit
from models import Pay

urlpatterns = pPatterns(
    (r'^$', pays, 3),
    (r'^edit\/(?P<id>\d+)\/$', editPay, 3),
    (r'^subedit\/$', subEdit, 3),
    *(
        (r'^api\/%s\/%s\/$' %  (i.cod, ii[0]), ii[1], 2) 
        for i in Pay.objects.filter(onl=True) 
            for ii in i.main.urls
    )
)