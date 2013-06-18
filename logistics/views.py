#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from consignee.forms import *
from purview.models import *
from order.models import *
from office.func import *
import time

from django.conf import settings

# Create your views here.

def logistics(request):

    c = request.GET.get('c') if request.GET.get('c') else 0
    s = request.GET.get('s')
    e = request.GET.get('e')
    k = request.GET.get('k') if request.GET.get('k') else ''
    p = int(request.GET.get('p')) if request.GET.get('p') > 0 else 1

    oStatus = OrderShip.sStatus

    oListAll = OrderInfo.objects.select_related().all()

    oList = page(l=oListAll, p=p)

    oList = logisticsPurview(oList, request).getElement().beMixed()

    return render_to_response('logistics.htm', locals(), context_instance=RequestContext(request))    



# 订单列表权限加持
class logisticsPurview:
    """首先获取当前角色可进行的订单操作权限. 其后获取订单的可选操作. 两者进行交集"""
    def __init__(self, oList, request):
        self.oList = oList
        self.role = OrderShip.sStatus

    # 获取订单可选操作项
    def getElement(self):

        for i in self.oList:
            if not i.ordership.shipStatus:

                i.action = (
                                (1, u'已发'), 

                            )
            elif i.i.ordership.shipStatus == 1:

                i.action = (
                                (2, u'拒签'), 
                                (3, u'已签'), 
                            )


            else:
                i.action = ()

        return self


    def beMixed(self):
        for i in self.oList:
            i.action = (i for i in i.action if i in self.role)

        return self.oList