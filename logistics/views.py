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

# 物流界面
def logcsUI(request):

    o = LogcsSerch(request)

    form = LogcsFrm(initial=o.initial)

    oList = o.search().chcs().range().page()
    oList = LogcsPur(oList, request).getOrds()
    oList = FncPur(oList, request).getOrds()
    oList = OrdPur(oList, request).getOrds()
    oList = ProPur(oList, request).getOrds()

    return render_to_response('logistics.htm', locals(), context_instance=RequestContext(request))

# 编辑物流界面
def editUI(request):
    from consignee.forms import conFrm

    form = conFrm(request)

    return render_to_response('logcsedit.htm', locals(), context_instance=RequestContext(request))

# 编辑物流前置操作
def editShip(request, c):
    sn = request.GET.get('sn')

    Ship(request).lCon(sn, c)

    from order.views import Ord

    Ord(request).cpyTsess(sn).cpyCongn(sn)
    
    return HttpResponseRedirect(request.paths[u'编辑物流'])

# 提交物流
def shipSub(request):

    return Ship(request).editSub()


# 物流状态修改
@conShip
def lCon(request, c):
    Ship(request).lCon(request.GET.get('sn'), c)

    return rdrBck(request)

# 止送
@conShip
def stopLogcs(request,c ):
    sn = request.GET.get('sn')
    Ship(request).lCon(sn, c)

    # from order.views import Ord
    # Ord(request).stopOrd(sn)

    return rdrBck(request)

# 非新单及编辑以外的订单操作
def lCons(request, c):
    c = int(c)
    
    _func = [lCon, editShip, lCon, lCon, stopLogcs]

    return _func[c](request, c)




class Ship(object):
    """
        物流管理 操作类
        
        用于物流状态修改以及提交物流

        只需实例后, 使用对应方法即可
        示例: Ship(request).editSub()

        订单数据来源为session中数据

        session['c'] = 联系人信息
        session['o'] = 订单基本信息, 比如订单类型, 新单或编辑

    """
    def __init__(self, request):
        self.request  = request
        from consignee.views import SpCnsgn
        self.c = SpCnsgn(self.request).c
        self.o = Ord(self.request).o

    def lCon(self, sn, c):
        from order.models import OrdInfo
        ship =  OrdInfo.objects.get(sn=sn).ordship

        ship.status = c

        ship.save()

        return self

    def editSub(self):
        messages.success(self.request, u'提交成功: %s' % self.o['sn'])

        return rdrRange(self.request.paths[u'物流'], self.c['date'], self.o['sn'])

class LogcsSerch(OrdSerch):
    """ 
        订单基本信息类

        存储于seesion数据的操作类

    """
    def __init__(self, request):
        super(LogcsSerch, self).__init__(request)

    def search(self):
        self.oList = self.baseSearch().oList.filter(ordsats__status__gt = 1)

        return self

    def chcs(self):
        if self.initial['c'] >= 0:
            self.oList = self.oList.filter(ordship__status=self.initial['c'])

        return self

    def range(self):
        self.oList = self.oList.filter(ordlogcs__date__range=(self.initial['s'], self.initial['e']))

        return self

# 订单列表权限加持
class LogcsPur(OrdPur):
    """
        首先获取当前角色可进行的订单操作权限. 

        其后获取订单的可选操作. 两者进行交集

    """
    def __init__(self, oList, request):
        super(LogcsPur, self).__init__(oList, request)
        self.path = request.paths[u'物流']

        ship = OrdShip
        self.chcs = ship.chcs
        self.action = ship.act

    # 获取订单可选操作项
    def getElement(self):
        for i in self.oList:
            if i.ordship.status < 2:
                i.form = AdvFrm(i)

            if not hasattr(i,'action'):
                i.action = {}

            i.action[self.path] = self.action[i.ordship.status]

        return self