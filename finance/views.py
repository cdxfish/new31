#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from new31.decorator import fncDetr
from order.views import OrdSerch, OrdPur


# Create your views here.

def fncUI(request):

    o = FncSerch(request)

    form = FncSrchFrm(initial=o.initial)

    oList = o.search().status().range().page()
    oList = FncPur(oList, request).getOrds()

    return render_to_response('financeui.htm', locals(), context_instance=RequestContext(request))


@fncDetr
def fCon(request, c):

    FncPrt(request).cCon(request.GET.get('sn'), c)

    return rdrtBck(request)

def fCons(request, c):
    c = int(c)
    return [fCon, fCon, fCon, fCon][c](request, c)


from new31.cls import BsSess
class FncSess(BsSess):
    """
        财务session类

    """
    def __init__(self, request):
        from payment.models import Pay

        self.s = 'f'

        try:
            pid = Pay.objects.getDefault().id
        except:
            pid = 0

        self.frmt = {
                        u'pay': pid,
            }
        super(FncSess, self).__init__(request)

    def getObj(self):
        from payment.models import Pay
        self.obj = self.f.copy()
        
        self.obj['pay'] = Pay.objects.getPayById(id=self.f['pay'])

        return self.obj
        

class FncPrt(object):
    """
        财务基本类

    """
    def __init__(self, request):
        self.request = request


    def cCon(self, sn, c):
        from order.models import Ord
        pay =  Ord.objects.get(sn=sn).fnc

        pay.status = c

        pay.save()

        return self



class FncSerch(OrdSerch):
    """
        对订单用财务搜索类

        用于订单条件过滤及显示
        继承自订单基本过滤类

    """
    def __init__(self, request):
        super(FncSerch, self).__init__(request)

    def search(self):
        self.oList = self.baseSearch().oList.filter(ord__status__gt = 1)

        return self

    def status(self):
        if self.initial['c'] >= 0:
            self.oList = self.oList.filter(ordship__status=self.initial['c'])

        return self

    def range(self):
        self.oList = self.oList.filter(logcs__date__range=(self.initial['s'], self.initial['e']))

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
        self.path = request.paths[u'财务']

        opay = OrdFnc
        self.chcs = opay.chcs
        self.action = opay.act

    # 获取订单可选操作项
    def getElement(self):

        for i in self.oList:
            if not hasattr(i,'action'):
                i.action = {}

            i.action[self.path] = self.action[i.fnc.status]

        return self