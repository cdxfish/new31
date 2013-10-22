#coding:utf-8
u"""生产"""
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.db.models import Q
from decorator import proDr
from new31.func import rdrtBck, page
from new31.cls import AjaxRJson
from message.decorator import msgDr
from message.models import Msg
# Create your views here.

def produce(request):
    u"""生产"""
    from forms import ProFrm

    o = ProSerch(request)

    if not request.GET.get('c'):
        o.initial['c'] = 1

    form = ProFrm(initial=o.initial)

    oList = o.get()
    oList = ProPur(oList, request).get()
    oList = sorted(oList, key=lambda x: x.logcs.advTime)

    return render_to_response('produceui.htm', locals(), context_instance=RequestContext(request))


def modifyPro(request, sn, s):
    u"""生产状态修改"""
    from models import Pro
    from purview.models import Role

    s = int(s)
    
    r = Role.objects
    p = Pro.objects.get(id=sn)
    _p = Pro.objects.cStatus(sn, s)

    return AjaxRJson().dumps({
        'sn': sn, 
        'act': r.getAjaxAct(r.getActByUser(request.user.id, p.act[s]), sn), 
        '_act': r.getAjaxAct(p.act[ p.status ], sn), 
        's': _p.status,
        'sStr': _p.get_status_display(),
        'obj': 'pro'
        })

@proDr
@msgDr
def nullPro(request, sn, s):
    u"""生产状态修改-> 生产未产"""    

    return modifyPro(request=request, sn=sn, s=s)
   
@proDr
@msgDr
def requirePro(request, sn, s):
    u"""生产状态修改-> 生产产求"""    

    return modifyPro(request=request, sn=sn, s=s)
  
@proDr
@msgDr
def duringPro(request, sn, s):
    u"""生产状态修改-> 生产产中"""    

    return modifyPro(request=request, sn=sn, s=s)

@proDr
@msgDr
def refusePro(request, sn, s):
    u"""生产状态修改-> 生产拒产"""    

    return modifyPro(request=request, sn=sn, s=s)

@proDr
@msgDr
def readyPro(request, sn, s):
    u"""生产状态修改-> 生产已产"""    

    return modifyPro(request=request, sn=sn, s=s)


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
        self.oList = self.baseSearch().oList.filter(Q(status=2) | Q(status=4)).order_by('-logcs__date', '-logcs__stime', '-logcs__advance', '-logcs__etime')

        return self

    def chcs(self):

        if self.initial['c'] >= 0:
            self.oList = self.oList.filter(pro__status=self.initial['c']).distinct()

        for i in self.oList:
            if self.initial['c'] >= 0:

                i.items = i.pro_set.filter(status=self.initial['c'])
            else:
                i.items = i.pro_set.all()

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
        for i in self.oList:
            if not hasattr(i, 'items'):
                i.items = i.pro_set.all()

        self.action = Pro.act

    def beMixed(self):

        for i in self.oList:
            for ii in i.items:
                ii.sn = ii.id
                if not hasattr(ii,'action'):
                    ii.action = []

                for iii in self.action[ii.status]:
                    try:
                        if iii[2] in self.role:
                            ii.action.append(iii)
                    except Exception, e:
                        # raise e
                        pass

        return self