#coding:utf-8
u"""物流"""
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib import messages
from new31.decorator import postDr
from decorator import logcsDr, dManDr
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
    # oList = ProPur(oList, request).get()
    oList = KpChng(oList, request).get()

    return render_to_response('logistics.htm', locals(), context_instance=RequestContext(request))

def baiduMap(request, address):
    u"""地图"""

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

    sList = sortList(oList, o.initial)

    form = LogcSrchFrm(initial=o.initial)

    return render_to_response('logcsview.htm', locals(), context_instance=RequestContext(request))


def sortList(oList, initial):
    u"""订单排序"""
    _oList = {}
    for i in oList:
        
        date = u'%s' % i.logcs.date
        lstime = u'%s - %s' % (i.logcs.stime.strftime('%H:%M'), i.logcs.etime.strftime('%H:%M'))
        advance = u'%s' % i.logcs.get_advance_display()

        if not date in _oList:
            _oList[date] = {}

        if not lstime in _oList[date]:
            _oList[date][lstime] = {}

        if not advance in _oList[date][lstime]:
            _oList[date][lstime][advance] = []

        _oList[date][lstime][advance].append(i)

    return _oList

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

    sn = OrdSess(request).sess['sn']

    logcs = Logcs.objects.get(ord=sn)

    Logcs.objects.saveLogcs(logcs.ord, request)

    messages.success(request, u'编辑成功: %s' % sn)

    return rdrRange(reverse('logistics:logcs'), LogcSess(request).sess['date'], sn)

@logcsDr
@dManDr
def modifyLogcs(request, sn, s):
    u"""物流状态修改"""
    from models import Logcs

    Logcs.objects.cStatus(sn, s)

    return rdrtBck(request)

def logcsUnsent(request, sn):
    u"""物流状态修改-> 物流未发"""

    return modifyLogcs(request, 0)

def logcsEdit(request, sn):
    u"""物流状态修改-> 物流编辑"""
    from models import Logcs
    from order.views import OrdSess

    sn = request.GET.get('sn')

    Logcs.objects.cStatus(sn, 1)
    LogcSess(request).copy(sn)

    OrdSess(request).cpyOrd(sn)
    
    return HttpResponseRedirect(reverse('logistics:logcsEditFrm'))

def logcsShip(request, sn):
    u"""物流状态修改-> 物流已发"""

    return modifyLogcs(request, 2)

def logcsRefused(request, sn):
    u"""物流状态修改-> 物流拒签"""

    return modifyLogcs(request, 3)

def logcsSign(request, sn):
    u"""物流状态修改-> 物流已签"""

    return modifyLogcs(request, 4)

@logcsDr
def logcsStop(request, sn):
    u"""物流状态修改-> 物流止送"""
    from models import Logcs
    # from order.models import Ord
    # from finance.models import Fnc
    from produce.models import Pro
    
    Logcs.objects.stop(sn)
    # Ord.objects.stop(sn)
    # Fnc.objects.stop(sn)
    Pro.objects.stop(sn)

    return rdrtBck(request)


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
        today = time.struct_time

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

        logcs = LogcSess(self.request)

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

        logcs.sess['user'] = u'%s' % oLogcs.ord.user
        logcs.sess['pay'] = oLogcs.ord.fnc.cod.id
        logcs.sess['consignee'] = u'%s' % oLogcs.consignee
        logcs.sess['area'] = area
        logcs.sess['address'] = u'%s' % oLogcs.address
        logcs.sess['tel'] = oLogcs.tel
        logcs.sess['date'] = u'%s' % oLogcs.date
        logcs.sess['time'] = time
        logcs.sess['note'] = u'%s' % oLogcs.note

        logcs._set()



from order.views import OrdSerch
class LogcsSerch(OrdSerch):
    """ 
        订单基本信息类

        存储于seesion数据的操作类

    """
    def __init__(self, request):
        super(LogcsSerch, self).__init__(request)

    def search(self):
        self.oList = self.baseSearch().oList.filter(Q(status=2) | Q(status=4))

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
            i.fee['total'] = Pro.objects.getFeeBySN(i.sn)

            i.fee['paid'] = keFrmt(i.fee['total'])

            i.fee['kpchng'] = i.fee['paid'] - i.fee['total']


        return self

    def get(self):

        return self.cntFee().oList

