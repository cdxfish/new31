#coding:utf-8
u"""物流"""
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib import messages
from new31.decorator import postDr
from new31.cls import AjaxRJson
from ajax.decorator import ajaxMsg
from log.decorator import ordLogDr
from message.decorator import msgDr
from message.models import Msg
from decorator import logcsDr, aLogcsDr
from new31.func import keFrmt, rdrtBck, rdrRange
import time,datetime

# Create your views here.

def logcs(request):
    u"""物流"""
    from forms import LogcSrchFrm
    from finance.views import FncPur
    from order.views import OrdPur
    from produce.views import ProPur

    o = LogcsSerch(request)

    form = LogcSrchFrm(initial=o.initial)

    oList = o.get()
    oList = LogcsPur(oList, request).get()
    oList = FncPur(oList, request).get()
    oList = OrdPur(oList, request).get()
    oList = ProPur(oList, request).get()
    oList = KpChng(oList, request).get()

    return render_to_response('logistics.htm', locals(), context_instance=RequestContext(request))

def logcsView(request):
    u"""物流安排"""
    from forms import LogcSrchFrm
    from finance.views import FncPur
    from order.views import OrdPur
    from produce.views import ProPur

    o = LogcsSerch(request)

    oList = o.get()
    oList = LogcsPur(oList, request).get()
    for i in oList:
        i.items = i.pro_set.filter(Q(sn__contains='33') | Q(sn__contains='44') | Q(sn__contains='55') | Q(sn__contains='77'))

    form = LogcSrchFrm(initial=o.initial)

    return render_to_response('logcsview.htm', locals(), context_instance=RequestContext(request))

def baiduMap(request):
    u"""地图"""

    address = request.GET.get('address', '')

    return render_to_response('baidumap.htm', locals(), context_instance=RequestContext(request))


def logcsEditFrm(request):
    u"""物流编辑表单"""
    from logistics.forms import logcsFrm

    logcs = logcsFrm(request)

    return render_to_response('logcsedit.htm', locals(), context_instance=RequestContext(request))

@postDr
def logcsSub(request):
    u"""物流编辑表单提交"""
    from order.views import OrdSess
    from models import Logcs
    from cart.views import CartSess
    from finance.views import FncSess
    
    sn = OrdSess(request).sess['sn']

    logcs = Logcs.objects.get(ord=sn)

    Logcs.objects.saveLogcs(logcs.ord, request)

    messages.success(request, u'物流编辑成功: %s' % sn)
    Msg.objects.success(u'物流编辑成功', {'sn': sn}, request.path)

    CartSess(request).clear()
    LogcSess(request).clear()
    OrdSess(request).clear()
    FncSess(request).clear()

    return rdrRange(reverse('logistics:logcs'), LogcSess(request).sess['date'], sn)


# @dManDr
@ordLogDr
def modifyLogcs(request, sn, s):
    u"""物流状态修改"""
    from models import Logcs
    from purview.models import Role

    s = int(s)
    l = Logcs.objects.get(ord__sn=sn)
    
    _l = Logcs.objects.cStatus(sn, s)

    r = Role.objects

    return AjaxRJson().dumps({
        'sn': sn, 
        'act': r.getAjaxAct(r.getActByUser(request.user.id, l.act[s]), sn), 
        '_act': r.getAjaxAct(l.act[ l.status ], sn), 
        's': _l.status,
        'sStr': _l.get_status_display(),
        'obj': 'logcs'
        })

@logcsDr(1)
@msgDr
def logcsUnsent(request, sn, s):
    u"""物流状态修改-> 物流未发"""

    return modifyLogcs(request=request, sn=sn, s=s)

@logcsDr()
@msgDr
def logcsEdit(request, sn, s):
    u"""物流状态修改-> 物流编辑"""
    from models import Logcs
    from order.views import OrdSess
    from finance.views import FncSess

    modifyLogcs(request=request, sn=sn, s=s)
    LogcSess(request).copy(sn)
    FncSess(request).copy(sn)

    OrdSess(request).cpyOrd(sn)
    
    return HttpResponseRedirect(reverse('logistics:logcsEditFrm'))

@logcsDr(1)
@msgDr
def logcsShip(request, sn, s):
    u"""物流状态修改-> 物流已发"""

    return modifyLogcs(request=request, sn=sn, s=s)

@logcsDr(1)
@msgDr
def logcsRefused(request, sn, s):
    u"""物流状态修改-> 物流拒签"""

    return modifyLogcs(request=request, sn=sn, s=s)

@logcsDr(1)
@msgDr
def logcsSign(request, sn, s):
    u"""物流状态修改-> 物流已签"""

    return modifyLogcs(request=request, sn=sn, s=s)

@logcsDr(1)
@msgDr
def logcsStop(request, sn, s):
    u"""物流状态修改-> 物流止送"""
    # from models import Logcs
    # from order.models import Ord
    # from finance.models import Fnc
    from produce.models import Pro
    
    # Logcs.objects.stop(sn)
    # Ord.objects.stop(sn)
    # Fnc.objects.stop(sn)
    Pro.objects.stop(sn)

    return modifyLogcs(request=request, sn=sn, s=s)

# @ajaxMsg('无法修改表单数据')
@aLogcsDr
@ordLogDr
@msgDr
def cDman(request, sn, user):
    u"""ajax-> 修改物流师傅"""
    from purview.models import Role
    from models import Logcs

    users = Role.objects.get(role=1).user.all()
    logcs = Logcs.objects.get(ord=sn)

    if user:
        from django.contrib.auth.models import User

        user = User.objects.get(id=user)

        if user in users:
            logcs.dman = user
        else:
            return  AjaxRJson().err(u'无法修改物流师傅')
    else:
        logcs.dman = None

    logcs.save()

    return AjaxRJson().dumps()

@ajaxMsg('无法修改表单数据')
@aLogcsDr
@ordLogDr
@msgDr
def cAdv(request, sn, value):
    u"""ajax-> 修改物流偏移量"""
    from models import Logcs
    sn = int(sn)
    value = int(value)
    advs = [i[0] for i in Logcs.advs]
    if not value in advs:
        return  AjaxRJson().err(u'无法修改修改物流偏移量')

    logcs = Logcs.objects.get(ord=sn)
    logcs.advance = value
    logcs.save()

    return AjaxRJson().dumps()


@ajaxMsg('无法填写表单')
def cLogcs(request):
    u"""ajax-> 修改收货人信息"""

    for i,v in request.GET.dict().items():
        LogcSess(request).setByName(i, u'%s' % v)

    return AjaxRJson().dumps()


from new31.cls import BsSess
class LogcSess(BsSess):
    """
        联系人信息
    """
    def __init__(self, request):
        from deliver.models import Deliver
        from area.models import Area
        from signtime.models import SignTime

        self.s = 'l'

        try:
            dlvrID = Deliver.objects.default().id
        except:
            dlvrID = 0

        try:
            areaID = Area.objects.default().id
        except:
            areaID = 0

        try:
            signID = SignTime.objects.default().id
        except:
            signID = 0
        
        self.frmt = {
                            'dlvr': dlvrID, 
                            'consignee': u'', 
                            'area': areaID, 
                            'address': u'', 
                            'tel': u'', 
                            'date': u'%s' % datetime.date.today(), 
                            'time': signID,
                            'note': u'',
                        } 

        super(LogcSess, self).__init__(request)
        

    def chkDate(self):
        date = time.strptime(self.sess['date'], u'%Y-%m-%d')
        today = time.strptime('%s' % datetime.date.today(), u'%Y-%m-%d')

        if today > date:
            self.sess['date'] = u'%s' % datetime.date.today()

        return self._set()


    def getObj(self):
        
        from deliver.models import Deliver
        from signtime.models import SignTime
        from area.models import Area

        self.obj = self.sess.copy()
        self.obj['dlvr'] = Deliver.objects.getDlvrById(id=self.sess[u'dlvr'])
        self.obj['time'] = SignTime.objects.getTimeById(id=self.sess[u'time'])
        self.obj['area'] = Area.objects.getAreaById(id=self.sess[u'area'])

        return self.obj


    def copy(self, sn):
        from models import Logcs
        from area.models import Area
        from signtime.models import SignTime

        oLogcs = Logcs.objects.get(ord__sn=sn)
 
        areas = oLogcs.area.split(' - ')

        try:
            area = Area.objects.get(name=areas[1]).id
        except Exception, e:
            area = Area.objects.default().id

        try:
            time = SignTime.objects.get(start=oLogcs.stime, end=oLogcs.etime).id
        except Exception, e:
            time = SignTime.objects.default().id

        self.sess['consignee'] = u'%s' % oLogcs.consignee
        self.sess['area'] = area
        self.sess['address'] = u'%s' % oLogcs.address
        self.sess['tel'] = oLogcs.tel
        self.sess['date'] = u'%s' % oLogcs.date
        self.sess['time'] = time
        self.sess['note'] = u'%s' % oLogcs.note

        return self._set()



from order.views import OrdSerch
class LogcsSerch(OrdSerch):
    """ 
        订单基本信息类

        存储于seesion数据的操作类

    """
    def __init__(self, request):
        super(LogcsSerch, self).__init__(request)

    def search(self):
        self.oList = self.baseSearch().oList.filter(Q(status=2) | Q(status=4)).order_by('-logcs__date', '-logcs__stime', 'logcs__area', 'logcs__address', '-sn' )
        return self

    def chcs(self):
        if self.initial['c'] >= 0:
            self.oList = self.oList.filter(logcs__status=self.initial['c'])

        return self

    def range(self):
        self.oList = self.oList.filter(logcs__date__range=(self.initial['s'], self.initial['e']))

        return self

# 订单列表权限加持
from purview.views import BsPur
class LogcsPur(BsPur):
    """
        首先获取当前角色可进行的订单操作权限. 

        其后获取订单的可选操作. 两者进行交集

    """
    def __init__(self, oList, request):
        from models import Logcs

        super(LogcsPur, self).__init__(oList, request)

        self.action = Logcs.act

    def beMixed(self):
        from forms import AdvFrm
        
        for i in self.oList:
            if i.logcs.status < 2:
                if 'logistics:cDman' in self.role:
                    i.form = AdvFrm(i)

            if not hasattr(i,'action'):
                i.action = []

            for ii in self.action[i.logcs.status]:
                try:
                    if ii[2] in self.role:
                        i.action.append(ii)
                except Exception, e:
                    # raise e
                    pass


        return self

class KpChng(object):
    """
        找零

    """
    def __init__(self, oList, request):
        self.oList = oList
        self.request = request
        self.fee = {
                    'paid': 0,
                    'total': 0,
                    'kpchng':0,
                }

    def cntFee(self):
        from produce.models import Pro

        for i in self.oList:
            i.fee = self.fee.copy()
            i.fee['total'] = Pro.objects.total(i.pro_set.all())

            i.fee['paid'] = keFrmt(i.fee['total'])

            i.fee['kpchng'] = i.fee['paid'] - i.fee['total']

        return self

    def get(self):

        return self.cntFee().oList