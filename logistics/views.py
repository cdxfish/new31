#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from new31.decorator import postDr
from decorator import logcsDr, dManDr
from new31.func import keFrmt, rdrtBck, rdrRange
import time,datetime

# Create your views here.

# 物流界面
def logcsUI(request):
    from forms import LogcSrchFrm
    from finance.views import FncPur
    from order.views import OrdPur
    from produce.views import ProPur

    o = LogcsSerch(request)

    form = LogcSrchFrm(initial=o.initial)

    oList = o.getOrds()
    oList = LogcsPur(oList, request).getOrds()
    oList = FncPur(oList, request).getOrds()
    oList = OrdPur(oList, request).getOrds()
    oList = ProPur(oList, request).getOrds()
    oList = KpChng(oList, request).getOrds()

    return render_to_response('logistics.htm', locals(), context_instance=RequestContext(request))

# 编辑物流界面
def editUI(request):
    from logistics.forms import logcsFrm

    logcs = logcsFrm(request)

    return render_to_response('logcsedit.htm', locals(), context_instance=RequestContext(request))

# 编辑物流前置操作
def editLogcs(request, s):
    from models import Logcs
    from order.views import OrdSess

    sn = request.GET.get('sn')

    Logcs.objects.cStatus(sn, s)
    LogcSess(request).copy(sn)

    OrdSess(request).cpyOrd(sn)
    
    return HttpResponseRedirect(request.paths[u'编辑物流'])

# 提交物流
@postDr
def logcsSub(request):
    from order.views import OrdSess
    from models import Logcs

    sn = OrdSess(request).sess['sn']

    logcs = Logcs.objects.get(ord=sn)

    Logcs.objects.saveLogcs(logcs.ord, request)

    messages.success(request, u'编辑成功: %s' % sn)

    return rdrRange(request.paths[u'物流'], LogcSess(request).sess['date'], sn)


# 物流状态修改
@logcsDr
@dManDr
def lCon(request, s):
    from models import Logcs

    Logcs.objects.cStatus(request.GET.get('sn'), s)

    return rdrtBck(request)

# 止送
@logcsDr
def stopLogcs(request, s):
    from models import Logcs
    from order.models import Ord

    sn = request.GET.get('sn')
    
    Logcs.objects.cStatus(sn, s)
    Ord.objects.stopOrd(sn)


    return rdrtBck(request)

# 非新单及编辑以外的订单操作
def lCons(request, s):
    s = int(s)

    return [lCon, editLogcs, lCon, lCon, lCon, stopLogcs][s](request, s)





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
                            'consignee':'', 
                            'area': areaID, 
                            'address':'', 
                            'tel':'', 
                            'date': '%s' % datetime.date.today(), 
                            'time': signID,
                            'note':'',
                        } 

        super(LogcSess, self).__init__(request)
        

    def chkDate(self):
        date = time.strptime(self.sess['date'], '%Y-%m-%d')
        today = time.struct_time

        if today > date:
            self.sess['date'] = '%s' % datetime.date.today()

        return self._set()


    def getObj(self):
        
        from deliver.models import Deliver
        from signtime.models import SignTime
        from area.models import Area

        self.obj = self.sess.copy()
        self.obj['dlvr'] = Deliver.objects.getDlvrById(id=self.sess['dlvr'])
        self.obj['time'] = SignTime.objects.getTimeById(id=self.sess['time'])
        self.obj['area'] = Area.objects.getAreaById(id=self.sess['area'])

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

        logcs.sess['user'] = oLogcs.ord.user
        logcs.sess['pay'] = oLogcs.ord.fnc.cod.id
        logcs.sess['consignee'] = oLogcs.consignee
        logcs.sess['area'] = area
        logcs.sess['address'] = oLogcs.address
        logcs.sess['tel'] = oLogcs.tel
        logcs.sess['date'] = '%s' % oLogcs.date
        logcs.sess['time'] = time
        logcs.sess['note'] = oLogcs.note

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
        self.oList = self.baseSearch().oList.filter(status__gt=1)

        return self

    def chcs(self):
        if self.initial['c'] >= 0:
            self.oList = self.oList.filter(logcs__status=self.initial['c'])

        return self

    def range(self):
        self.oList = self.oList.filter(logcs__date__range=(self.initial['s'], self.initial['e']))

        return self

# 订单列表权限加持
from order.views import OrdPur
class LogcsPur(OrdPur):
    """
        首先获取当前角色可进行的订单操作权限. 

        其后获取订单的可选操作. 两者进行交集

    """
    def __init__(self, oList, request):
        from models import Logcs

        super(LogcsPur, self).__init__(oList, request)

        self.path = request.paths[u'物流']

        self.chcs = Logcs.chcs
        self.action = Logcs.act

    # 获取订单可选操作项
    def getElement(self):
        from forms import AdvFrm

        for i in self.oList:
            if i.logcs.status < 2:
                i.form = AdvFrm(i)

            if not hasattr(i,'action'):
                i.action = {}

            i.action[self.path] = self.action[i.logcs.status]

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
            i.fee['total'] = Pro.objects.getFeeBySN(i.sn)

            i.fee['paid'] = keFrmt(i.fee['total'])

            i.fee['kpchng'] = i.fee['paid'] - i.fee['total']


        return self

    def getOrds(self):

        return self.cntFee().oList

