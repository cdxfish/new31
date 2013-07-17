#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from models import *
from forms import *
from order.views import *
from purview.views import *
from signtime.models import *

# Create your views here.

def produceUI(request):

    o = ProSerch(request)

    form = ProduceForm(initial=o.initial)

    oList = o.search().range().chcs().page()
    oList = ProPur(oList, request).getElement().beMixed()

    oList = sortList(oList)

    return render_to_response('produceui.htm', locals(), context_instance=RequestContext(request))


def sortList(oList):
    _oList = {}
    for i in oList:
        
        signDate = u'%s' % i.orderlogistics.signDate
        logisTimeStart = u'%s' % i.orderlogistics.logisTimeStart
        advance = u'%s' % i.orderlogistics.get_advance_display()

        i.items = [ ii for ii in i.items if ii.produce.status ]

        if i.items:

            if not signDate in _oList:
                _oList[signDate] = {}

            if not logisTimeStart in _oList[signDate]:
                _oList[signDate][logisTimeStart] = {}

            if not advance in _oList[signDate][logisTimeStart]:
                _oList[signDate][logisTimeStart][advance] = []

            _oList[signDate][logisTimeStart][advance].append(i)

    return _oList



def pCon(request, c):

    c = int(c)
    sn = request.GET.get('sn')
    item =  Produce.objects.get(item=sn)

    item.status = c

    item.save()

    return redirectBack(request)



class ProSerch(OrderSerch):
    """ 
        生产管理类

        用于工厂操作商品生产用

    """
    def __init__(self, request):
        super(ProSerch, self).__init__(request)

    def search(self):
        self.oList = self.baseSearch().oList.filter(orderstatus__status__gt = 1)

        return self

    def chcs(self):
        for i in self.oList:
            items = []
            for ii in i.orderitem_set.all():
                if self.initial['c'] >= 0:
                    if ii.produce.status == self.initial['c']:
                        items.append(ii)
                else:
                    items.append(ii)

            i.items = items

        return self

    def range(self):
        self.oList = self.oList.filter(orderlogistics__signDate__range=(self.initial['s'], self.initial['e']))

        return self

    def page(self):
        return page(l=self.oList, p=int(self.request.GET.get('p', 1)))


# 订单列表权限加持
class ProPur(OrdPur):
    """
        首先获取当前角色可进行的订单操作权限. 

        其后获取订单的可选操作. 两者进行交集.

    """
    def __init__(self, oList, request):
        super(ProPur, self).__init__(oList, request)
        self.chcs = Produce.chcs
        self.path = request.paths[u'生产']
        self.action = (
                    ((1, u'产求'), ),
                    ((2, u'产中'), (3, u'拒产'), ),
                    ((3, u'拒签'), (4, u'已产'), ),
                    ((1, u'产求'), ),
                    (),
                )

        for i in self.oList:
            i.items = i.orderitem_set.all()


    # 获取订单可选操作项
    def getElement(self):
        for i in self.oList:
            items = []

            for ii in i.items:
                if not hasattr(ii,'action'):
                    ii.action = {}

                try:
                    status = ii.produce.status
                except Exception, e:
                    status = Produce.objects.create(item=ii).status #关联外键

                ii.action[self.path] = self.action[status]

                items.append(ii)

            i.items = items

        return self


    def beMixed(self):
        for i in self.oList:
            for ii in i.items:
                ii.action[self.path] = tuple([ iii for iii in ii.action[self.path] if iii in self.chcs ])

        return self.oList