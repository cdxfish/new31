#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from new31.decorator import proDetr
from order.views import OrdSerch, OrdPur


# Create your views here.

def produceUI(request):

    o = ProSerch(request)

    form = ProFrm(initial=o.initial)

    oList = o.search().range().chcs().page()
    oList = ProPur(oList, request).getElement().beMixed().oList

    oList = sortList(oList)

    return render_to_response('produceui.htm', locals(), context_instance=RequestContext(request))


def sortList(oList):
    _oList = {}
    for i in oList:
        
        date = u'%s' % i.logcs.date
        lstime = u'%s' % i.logcs.lstime
        advance = u'%s' % i.logcs.get_advance_display()

        i.items = [ ii for ii in i.items if ii.produce.status ]

        if i.items:

            if not date in _oList:
                _oList[date] = {}

            if not lstime in _oList[date]:
                _oList[date][lstime] = {}

            if not advance in _oList[date][lstime]:
                _oList[date][lstime][advance] = []

            _oList[date][lstime][advance].append(i)

    return _oList


@proDetr
def pCon(request, c):
    ProCon(request).cCon(request.GET.get('sn'), c)

    return rdrtBck(request)

def pCons(request, c):
    c = int(c)

    return [pCon, pCon, pCon, pCon, pCon][c](request, c)


class ProCon(object):
    """
        生产状态操作类




    """
    def __init__(self, request):
        self.request = request


    def cCon(self, sn, c):
        item = Pro.objects.get(item=sn)

        item.status = c

        item.save()

        return self


class ProSerch(OrdSerch):
    """ 
        工厂订单搜索类

        继承于基本订单搜索类
        前期对订单基本搜索后转入此类进行二次搜索

    """
    def __init__(self, request):
        super(ProSerch, self).__init__(request)

    def search(self):
        self.oList = self.baseSearch().oList.filter(ord__status__gt = 1)

        return self

    def chcs(self):
        for i in self.oList:
            items = []
            for ii in i.orditem_set.all():
                if self.initial['c'] >= 0:
                    if ii.produce.status == self.initial['c']:
                        items.append(ii)
                else:
                    items.append(ii)

            i.items = items

        return self

    def range(self):
        self.oList = self.oList.filter(logcs__date__range=(self.initial['s'], self.initial['e']))

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
        pro = Pro
        self.chcs = pro.chcs
        self.path = request.paths[u'生产']
        self.action = pro.act

        for i in self.oList:
            i.items = i.orditem_set.all()


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
                    status = Pro.objects.create(item=ii).status #关联外键

                ii.action[self.path] = self.action[status]

                items.append(ii)

            i.items = items

        return self

    def beMixed(self):
        for i in self.oList:
            for ii in i.items:
                ii.action[self.path] = tuple([ iii for iii in ii.action[self.path] if u'%s%s/' % (self.path, iii[0]) in self.role ])

        return self

    def mixedStatus(self):
        for i in self.oList:
            for ii in i.items:
                ii.action[self.path] = tuple([ iii for iii in ii.action[self.path] if iii in self.chcs ])

        return self