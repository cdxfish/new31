#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from consignee.forms import *
from purview.models import *
from purview.views import *
from order.models import *
from order.views import *
from finance.views import *
from new31.func import *
from forms import *
import time,datetime

from django.conf import settings

# Create your views here.

def logisticsUI(request):

    o = Logistics(request)

    form = LogisticsForm(initial=o.initial)

    oList = o.search().oStatus().range().page()
    oList = logisticsPurview(oList, request).getElement().beMixed()
    oList = FinancePurview(oList, request).getElement().beMixed()
    oList = OrderPurview(oList, request).beMixed()

    return render_to_response('logistics.htm', locals(), context_instance=RequestContext(request))    

# 物流信息提交
def cCon(request, c):

    c = int(c)
    orderSN = request.GET.get('sn')
    order =  OrderShip.objects.get(order=orderSN)

    order.shipStatus = c

    order.save()

    if c > 1:
        return redirectBack(request)

    else:
        # 将订单信息配置到seesion当中
        ShipConsignee(request).setSiessionByOrder(sn=orderSN)
        Order(request).setSeesion(OrderInfo.objects.get(orderSn=orderSN).orderType)

        return HttpResponseRedirect(request.paths[u'新订单'])

class Logistics(Order):
    """ 
        订单基本信息类

        存储于seesion数据的操作类

    """
    def __init__(self, request):
        super(Logistics, self).__init__(request)

    def search(self):
        self.oList = self.baseSearch().oList.filter(orderstatus__status__gt = 1)

        return self

    def oStatus(self):
        if self.initial['c'] >= 0:
            self.oList = self.oList.filter(ordership__status=self.initial['c'])

        return self

    def range(self):
        self.oList = self.oList.filter(orderlogistics__signDate__range=(self.initial['s'], self.initial['e']))

        return self

    def page(self):
        return page(l=self.oList, p=int(self.request.GET.get('p', 1)))


# 订单列表权限加持
class logisticsPurview:
    """
        首先获取当前角色可进行的订单操作权限. 

        其后获取订单的可选操作. 两者进行交集

    """
    def __init__(self, oList, request):
        self.oList = oList
        self.oStatus = OrderShip.oStatus
        self.path = request.paths[u'物流']

    # 获取订单可选操作项
    def getElement(self):
        for i in self.oList:
            i.form = AdvanForm(i)
            if not hasattr(i,'action'):
                i.action = {}

            if i.ordership.status < 2:

                i.action[self.path] = (
                                (1, u'编辑'), 
                                (2, u'已发'), 

                            )
            elif i.ordership.status == 2:

                i.action[self.path] = (
                                (3, u'拒签'), 
                                (4, u'已签'), 
                            )


            else:
                i.action[self.path] = ()

        return self


    def beMixed(self):
        for i in self.oList:
            i.action[self.path] = tuple([ ii for ii in i.action[self.path] if ii in self.oStatus ])

        return self.oList