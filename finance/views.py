#coding:utf-8
u"""财务"""
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from decorator import fncDetr
from new31.func import rdrtBck


# Create your views here.

def fnc(request):
    u"""财务"""
    from forms import FncSrchFrm

    o = FncSerch(request)

    form = FncSrchFrm(initial=o.initial)

    oList = o.get()
    oList = FncPur(oList, request).get()

    return render_to_response('financeui.htm', locals(), context_instance=RequestContext(request))


@fncDetr
def modifyFnc(request, sn, s):
    u"""财务操作"""
    from models import Fnc

    Fnc.objects.cStatus(sn, s)
    
    return rdrtBck(request)

def unpaidFnc(request, sn):
    u"""财务状态修改-> 财务未付"""

    return modifyFnc(request, sn, 0)

def paidFnc(request, sn):
    u"""财务状态修改-> 财务已付"""

    return modifyFnc(request, sn, 1)

def closedFnc(request, sn):
    u"""财务状态修改-> 财务已结"""

    return modifyFnc(request, sn, 2)

def checkedFnc(request, sn):
    u"""财务状态修改-> 财务已核"""

    return modifyFnc(request, sn, 3)

def stopFnc(request, sn):
    u"""财务状态修改-> 财务止付"""

    return modifyFnc(request, sn, 4)


from new31.cls import BsSess
class FncSess(BsSess):
    """
        财务session类

    """
    def __init__(self, request):
        from payment.models import Pay

        self.s = 'f'

        try:
            pid = Pay.objects.default().id
        except:
            pid = 0

        self.frmt = {
                        u'pay': pid,
            }
        super(FncSess, self).__init__(request)

    def getObj(self):
        from payment.models import Pay
        
        self.obj = self.sess.copy()
        
        self.obj['pay'] = Pay.objects.getPayById(id=self.sess['pay'])

        return self.obj
        

from order.views import OrdSerch
class FncSerch(OrdSerch):
    """
        对订单用财务搜索类

        用于订单条件过滤及显示
        继承自订单基本过滤类

    """
    def __init__(self, request):
        super(FncSerch, self).__init__(request)

    def search(self):
        self.oList = self.baseSearch().oList.filter(status__gt = 1)

        return self

    def chcs(self):
        if self.initial['c'] >= 0:

            self.oList = self.oList.filter(fnc__status=self.initial['c'])

        return self

    def range(self):
        self.oList = self.oList.filter(logcs__date__range=(self.initial['s'], self.initial['e']))

        return self


# 订单列表权限加持
from purview.views import BsPur
class FncPur(BsPur):
    """
        首先获取当前角色可进行的订单操作权限. 

        其后获取订单的可选操作. 两者进行交集

    """
    def __init__(self, oList, request):
        from models import Fnc
        super(FncPur, self).__init__(oList, request)

        self.action = Fnc.act

    def beMixed(self):
        
        for i in self.oList:

            if not hasattr(i,'action'):
                i.action = []

            for ii in self.action[i.fnc.status]:
                try:
                    if ii[2] in self.role:
                        i.action.append(ii)
                except Exception, e:
                    # raise e
                    pass


        return self