#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from consignee.forms import *
from purview.models import *
from purview.views import *
from order.models import *
from order.views import *
from produce.views import *
from finance.views import *
from new31.func import *
from forms import *
import time,datetime

from django.conf import settings

# Create your views here.

def logisticsUI(request):

    o = LogcsSerch(request)

    form = LogcsForm(initial=o.initial)

    oList = o.search().chcs().range().page()
    oList = OrdPur(oList, request).getOrds()
    oList = LogcsPur(oList, request).getOrds()
    oList = FncPur(oList, request).getOrds()
    oList = ProPur(oList, request).getOrds()

    return render_to_response('logistics.htm', locals(), context_instance=RequestContext(request))    

# 物流信息提交
def lCon(request, c):

    c = int(c)
    orderSN = request.GET.get('sn')
    order =  OrdShip.objects.get(order=orderSN)

    order.status = c

    order.save()

    if c > 1:
        return redirectBack(request)

    else:
        # 将订单信息配置到seesion当中
        SpCnsgn(request).setSiessionByOrd(sn=orderSN)
        Ord(request).setSeesion(OrdInfo.objects.get(orderSn=orderSN).typ)

        return HttpResponseRedirect(request.paths[u'新订单'])

class LogcsSerch(OrdSerch):
    """ 
        订单基本信息类

        存储于seesion数据的操作类

    """
    def __init__(self, request):
        super(LogcsSerch, self).__init__(request)

    def search(self):
        self.oList = self.baseSearch().oList.filter(orderstatus__status__gt = 1)

        return self

    def chcs(self):
        if self.initial['c'] >= 0:
            self.oList = self.oList.filter(ordership__status=self.initial['c'])

        return self

    def range(self):
        self.oList = self.oList.filter(orderlogistics__signDate__range=(self.initial['s'], self.initial['e']))

        return self

# 订单列表权限加持
class LogcsPur(OrdPur):
    """
        首先获取当前角色可进行的订单操作权限. 

        其后获取订单的可选操作. 两者进行交集

    """
    def __init__(self, oList, request):
        super(LogcsPur, self).__init__(oList, request)
        self.chcs = OrdShip.chcs
        self.path = request.paths[u'物流']
        self.action = (
                        ((1, u'编辑'), (2, u'已发'),),
                        ((1, u'编辑'), (2, u'已发'),),
                        ((3, u'拒签'),(4, u'已签'),),
                    )

    # 获取订单可选操作项
    def getElement(self):
        for i in self.oList:
            i.form = AdvanForm(i)
            if not hasattr(i,'action'):
                i.action = {}

            i.action[self.path] = self.action[i.ordship.status]

        return self