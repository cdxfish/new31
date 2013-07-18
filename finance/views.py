#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from forms import *
from signtime.models import *
from order.views import *

# Create your views here.

def financeUI(request):

    o = FncSearch(request)

    form = financeForm(initial=o.initial)

    oList = o.search().status().range().page()
    oList = FncPur(oList, request).getOrders()
    oList = OrdPur(oList, request).getOrders()

    return render_to_response('financeui.htm', locals(), context_instance=RequestContext(request))


class FncSearch(OrderSerch):
    """
        财务基本类

        用于订单条件过滤及显示
        继承自订单基本过滤类

    """
    def __init__(self, request):
        super(FncSearch, self).__init__(request)

    def search(self):
        self.oList = self.baseSearch().oList.filter(orderstatus__status__gt = 1)

        return self

    def status(self):
        if self.initial['c'] >= 0:
            self.oList = self.oList.filter(ordership__status=self.initial['c'])

        return self

    def range(self):
        self.oList = self.oList.filter(orderlogistics__signDate__range=(self.initial['s'], self.initial['e']))

        return self

    def page(self):
        return page(l=self.oList, p=int(self.request.GET.get('p', 1)))


# 订单列表权限加持
class FncPur(OrdPur):
    """
        首先获取当前角色可进行的订单操作权限. 

        其后获取订单的可选操作. 两者进行交集

    """
    def __init__(self, oList, request):
        super(FncPur, self).__init__(oList, request)
        self.chcs = OrderPay.chcs
        self.path = request.paths[u'财务']
        self.action = (
                        ((1, u'已付'),),
                        ((1, u'已付'),),
                        ((2, u'已结'),),
                        ((3, u'已核'),),
                )

    # 获取订单可选操作项
    def getElement(self):


        for i in self.oList:
            if not hasattr(i,'action'):
                i.action = {}

            i.action[self.path] = self.action[i.orderpay.status]

        return self