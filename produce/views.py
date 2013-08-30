#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from decorator import proDr
from new31.func import rdrtBck, page


# Create your views here.

def produce(request):
    u"""生产: 生产"""
    from forms import ProFrm

    o = ProSerch(request)

    form = ProFrm(initial=o.initial)

    oList = o.get()
    oList = ProPur(oList, request).get()

    oList = sortList(oList, o.initial)

    return render_to_response('produceui.htm', locals(), context_instance=RequestContext(request))

def sortList(oList, initial):
    u"""生产: 订单排序"""
    _oList = {}
    for i in oList:
        
        date = u'%s' % i.logcs.date
        lstime = u'%s' % i.logcs.lstime
        advance = u'%s' % i.logcs.get_advance_display()

        _items = []

        if not hasattr(i, 'items'):
            i.items = i.pro_set.all()

        for ii in i.items:
            if initial['c'] >= 0:
                if ii.status == initial['c']:
                    _items.append(ii)
            else:
                _items.append(ii)

            i.items = _items


        if i.items:

            if not date in _oList:
                _oList[date] = {}

            if not lstime in _oList[date]:
                _oList[date][lstime] = {}

            if not advance in _oList[date][lstime]:
                _oList[date][lstime][advance] = []

            _oList[date][lstime][advance].append(i)

    return _oList

@proDr
def modifyPro(request, s):
    u"""生产: 生产状态修改"""
    from models import Pro

    Pro.objects.cStatus(request.GET.get('id'), s)

    return rdrtBck(request)

def nullPro(request):
    u"""生产: 生产状态修改-> 生产未产"""    

    return modifyPro(request, 0)
    
def requirePro(request):
    u"""生产: 生产状态修改-> 生产产求"""    

    return modifyPro(request, 1)
    
def duringPro(request):
    u"""生产: 生产状态修改-> 生产产中"""    

    return modifyPro(request, 2)

def refusePro(request):
    u"""生产: 生产状态修改-> 生产拒产"""    

    return modifyPro(request, 3)

def readyPro(request):
    u"""生产: 生产状态修改-> 生产已产"""    

    return modifyPro(request, 4)


from order.views import OrdSerch
class ProSerch(OrdSerch):
    """ 
        工厂订单搜索类

        继承于基本订单搜索类
        前期对订单基本搜索后转入此类进行二次搜索

    """
    def __init__(self, request):
        super(ProSerch, self).__init__(request)

    def search(self):
        self.oList = self.baseSearch().oList.filter(Q(status=2) | Q(status=4))

        return self

    def chcs(self):

        if self.initial['c'] >= 0:
            self.oList = self.oList.filter(pro__status=self.initial['c'])

        return self

    def range(self):
        self.oList = self.oList.filter(logcs__date__range=(self.initial['s'], self.initial['e']))
        

        return self


# 订单列表权限加持
from purview.views import BsPur
class ProPur(BsPur):
    """
        首先获取当前角色可进行的订单操作权限. 

        其后获取订单的可选操作. 两者进行交集.

    """
    def __init__(self, oList, request):
        from models import Pro

        super(ProPur, self).__init__(oList, request)
        self.path = request.pPath[u'生产']

        pro = Pro
        self.chcs = pro.chcs
        self.action = pro.act

        for i in self.oList:
            i.items = i.pro_set.all()


    # 获取订单可选操作项
    def getElement(self):
        from models import Pro

        for i in self.oList:
            items = []

            for ii in i.items:
                if not hasattr(ii,'action'):
                    ii.action = {}

                ii.action[self.path] = self.action[ii.status]
                ii.optr = 'id'
                ii.value = ii.id

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