#coding:utf-8
u"""订单"""
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect
from new31.decorator import postDr, rdrtBckDr, timeit
from new31.func import frMtFee, rdrRange, page, rdrtBck, f02f
from new31.cls import AjaxRJson
from ajax.decorator import ajaxMsg
from log.decorator import ordLogDr
from cart.decorator import checkCartDr
from decorator import ordDr, subMsg, subDr, modifyDr
from logistics.decorator import chLogcsDr
from finance.decorator import chFncDr
from decimal import Decimal
import time, datetime, re

# Create your views here.
# @timeit
def ords(request):
    u"""订单"""
    from forms import OrdSrchFrm
    from logistics.views import KpChng

    o = OrdSerch(request)
    oList = o.get()
    oList = OrdPur(oList, request).get()
    oList = KpChng(oList, request).get()

    form = OrdSrchFrm(initial=o.initial)

    return render_to_response('orderlist.htm', locals(), context_instance=RequestContext(request))

def viewOrd(request, sn):
    u"""查看订单"""
    from order.models import Ord
    from produce.models import Pro

    o = Ord.objects.get(sn=sn)
    o.total = Pro.objects.getFeeBySN(sn)

    return render_to_response('orderview.htm', locals(), context_instance=RequestContext(request))

@postDr
@checkCartDr
@chLogcsDr
@chFncDr
@subDr
def submitOrd(request):
    u"""订单提交"""
    from logistics.views import LogcSess

    logcs = LogcSess(request).setByDict(request.POST.dict())

    o = OrdSub(request).submit()

    if o.error:
        return o.showError()
    else:
        messages.success(request, u'订单提交成功: %s' % o.sn)

        return rdrRange(reverse('order:ords'), '%s' % datetime.date.today(), o.sn)

def newOrdFrm(request):
    u"""新单表单"""
    OrdSess(request).setSzero()

    return editOrdFrm(request)

def editOrdFrm(request):
    u"""订单编辑表单"""
    from cart.views import CartSess
    from forms import ItemsForm, ordFrm
    from logistics.forms import logcsFrm
    from finance.forms import fncFrm

    items = CartSess(request).show()

    ItemsForm.getItemForms(items['items'])

    logcs = logcsFrm(request)
    fnc = fncFrm(request)

    ord = ordFrm(request)

    return render_to_response('orderneworedit.htm', locals(), context_instance=RequestContext(request))

@ordDr(1)
def modifyOrd(request, sn, s):
    u"""订单状态修改"""
    from models import Ord
    from purview.models import Role

    o = Ord.objects.get(sn=sn)
    _o = Ord.objects.cStatus(sn, s)

    r = Role.objects

    return AjaxRJson().dumps({
        'sn': sn, 
        'act': r.getAjaxAct(r.getActByUser(request.user.id, o.act[s]), sn), 
        '_act': r.getAjaxAct(o.act[ o.status ], sn), 
        's': _o.status,
        'sStr': _o.get_status_display(),
        'obj': 'ord'
        })


def copyOrd(request, sn):
    u"""订单复制"""
    OrdSess(request).copy(int(sn))

    return HttpResponseRedirect(reverse('order:newOrdFrm'))

@ordLogDr
@modifyDr(1)
@ordDr()
def editOrd(request, sn, i):
    u"""订单状态修改-> 订单编辑"""
    from models import Ord
    Ord.objects.cStatus(sn, i)

    OrdSess(request).copy(sn)

    return HttpResponseRedirect(reverse('order:editOrdFrm'))

@ordLogDr
def confirmOrd(request, sn):
    u"""订单状态修改-> 订单确认"""

    return modifyOrd(request, sn, 2)

@ordLogDr
def nullOrd(request, sn):
    u"""订单状态修改-> 订单无效"""

    return modifyOrd(request, sn, 3)

@ordLogDr
def stopOrd(request, sn):
    u"""订单状态修改-> 订单止单"""

    return modifyOrd(request, sn, 4)

@postDr
@rdrtBckDr('无法添加商品，部分商品已下架。')
def addItemOrd(request):
    u"""添加商品"""
    from cart.views import CartSess

    CartSess(request).pushByIDs(request.POST.getlist('i'))
    return rdrtBck(request)

@rdrtBckDr('无法删除商品，请与管理员联系。')
def delItemOrd(request, mark):
    u"""删除商品"""
    from cart.views import CartSess

    CartSess(request).delete(int(mark))

    return rdrtBck(request)


@ajaxMsg('无法修改表单数据')
def cItem(request):
    u"""ajax-> 修改购物车内商品"""
    from cart.views import CartSess
    mark = int(request.GET.get('mark')[1:])
    cc = CartSess(request).chngItem()

    i = cc.getItem(mark)

    return AjaxRJson().dumps({
        'mark': mark,
        'fee': f02f(i['fee']),
        'nfee': f02f(i['nfee']),
        'st': f02f(i['total']),
        'total': f02f(cc.total()),
    })


@ajaxMsg('未找到商品')
def getItemByKeyword(request):
    u"""ajax-> 商品查询"""
    from item.models import Item

    r = [ { 'name':i.name, 'sn': i.sn, 'id': i.id, } for i in Item.objects.likeNameOrSn(request.GET.get('k', ''))]

    return AjaxRJson().dumps(r)

@ajaxMsg('无此会员')
def getUser(request):
    u"""ajax-> 查询会员"""
    from account.models import BsInfo

    u = BsInfo.objects.get(user__username=request.GET.get('u'))

    return AjaxRJson().dumps({
            u'用户名': u.user.username,
            u'姓名': '%s %s' % (u.user.last_name, u.user.first_name),
            u'生日': '%s %s' % (u.get_mon_display(), u.get_day_display()),
            u'性别': u.get_sex_display(),
            u'类型': u.get_typ_display(),
            u'邮箱': u.user.email,
            u'积分': u.user.pts.pt,
            u'注册时间': '%s' % u.user.date_joined,
        })

@ajaxMsg('无法填写表单')
def cOrd(request):
    u"""ajax-> 修改订单信息"""
    for i,v in request.GET.dict().items():
        OrdSess(request).setByName(i, v)

    return AjaxRJson().dumps()

from new31.cls import BsSess
class OrdSess(BsSess):
    """ 
        订单基本信息类

        存储于seesion数据的操作类

    """
    def __init__(self, request):
        from models import Ord

        self.s = 'o'
        self.frmt =  {
                        'typ': Ord.typs[0][0],
                        'status': Ord.chcs[0][0],
                        'sn': 0,
                        'user': '',
            }

        super(OrdSess, self).__init__(request)

    def setUser(self):
        self.sess['user'] = self.request.user.username

        return self._set()


    def setSzero(self):
        self.sess['status'] = 0

        return self._set()


    def setSone(self):
        self.sess['status'] = 1

        return self._set()


    def copy(self, sn):

        return self.cpyOrd(sn).cpyLogcs(sn).cpyFnc(sn).cpyItem(sn)


    def cpyOrd(self, sn):
        from models import Ord
        
        order = Ord.objects.get(sn=sn)
        self.sess['typ'] = order.typ
        self.sess['sn'] = sn
        self.sess['user'] = order.user

        return self.setSone()


    def cpyLogcs(self, sn):
        from logistics.views import LogcSess

        LogcSess(self.request).copy(sn)

        return self

    def cpyItem(self, sn):
        from cart.views import CartSess

        CartSess(self.request).copy(sn)

        return self

    def cpyFnc(self, sn):
        from finance.views import FncSess

        FncSess(self.request).copy(sn)

        return self


class OrdSerch(object):
    """
        订单基本搜索类

    """
    def __init__(self, request):
        from models import Ord

        self.request = request

        self.oList = Ord.objects.select_related().all()

        today = datetime.date.today()
        oneDay = datetime.timedelta(days=1)

        self.initial = {
                        'o': int(request.GET.get('o', -1)),
                        'c': int(request.GET.get('c', 0)), 
                        's': request.GET.get('s', '%s' % today).strip(),
                        'e': request.GET.get('e', '%s' % (today + oneDay)).strip(),
                        # 'e': request.GET.get('e', '%s' % today).strip(),
                        'k': request.GET.get('k', '').strip(), 
            }

        
    def baseSearch(self):
        if re.search(ur'\d{4}\-\d{2}\-\d{2}', self.initial['k']):
            self.oList = self.oList.filter(logcs__date=self.initial['k'])
        else:

            self.oList = self.oList.filter(
                    Q(sn__contains=self.initial['k']) |
                    Q(user__username__contains=self.initial['k']) |
                    Q(logcs__consignee__contains=self.initial['k']) |
                    Q(logcs__area__contains=self.initial['k']) |
                    Q(logcs__address__contains=self.initial['k']) |
                    Q(logcs__tel__contains=self.initial['k']) |
                    Q(logcs__stime__contains=self.initial['k']) |
                    Q(logcs__etime__contains=self.initial['k']) |
                    Q(logcs__note__contains=self.initial['k']) |
                    Q(logcs__dman__last_name__contains=self.initial['k']) |
                    Q(logcs__dman__first_name__contains=self.initial['k'])
                )

        if self.initial['o'] >= 0:
            self.oList = self.oList.filter(typ=self.initial['o'])

        return self

    def search(self):

        return self

    def chcs(self):
        if self.initial['c'] >= 0:
            self.oList = self.oList.filter(status=self.initial['c'])

        return self

    def range(self):

        self.oList = self.oList.filter((Q(ordlog__act='order:submitOrd') | Q(ordlog__act='order:editOrd')), ordlog__time__range=(self.initial['s'], self.initial['e']) ).distinct()

        return self

    def page(self):

        return page(l=self.oList, p=int(self.request.GET.get('p', 1)))

    def get(self):

        return self.baseSearch().search().range().chcs().page()


from purview.views import BsPur
class OrdPur(BsPur):
    """
        订单列表权限加持

        获取当前角色可进行的订单操作权限.
        获取订单状态,判定可选权限.
        两者进行交集操作.

    """

    def __init__(self, oList, request):
        from models import Ord

        super(OrdPur, self).__init__(oList, request)

        self.action = Ord.act

class OrdSub(object):
    """ 
        订单提交类.

        订单提交只需实例后, 使用 <<submit>> 方法即可
        示例: OrdSubmit(request).submit()

        订单数据来源为session中数据

        session['c'] = 商品信息
        session['l'] = 联系人信息
        session['o'] = 订单基本信息, 比如订单类型, 新单或编辑



        此类已根据 setting.DEBUG 对类方法进行了 <<用户级提示>> 装饰
        当 settings.DEBUG = True 时, 用户级提示关闭, 反之开启.

    """
    def __init__(self, request):
        self.request = request
        self.error = False

        self.o = OrdSess(self.request).sess


    def submit(self):

        if self.o['status']:
            self.editOrdFmt()

        else:
            self.newSn()

        self.pushOrd()
        self.logcs()
        self.pro()
        self.fnc()
        self.log()
        self.done()

        return self

    # 获得新的订单编号
    def getNewOrdSn(self):
        t = time.gmtime()
        tCount = int('%02d%02d%02d' % (t.tm_hour,t.tm_min, t.tm_sec))
        sExpiryDate = self.request.session.get_expiry_date()
        sCount = (sExpiryDate.hour * sExpiryDate.minute * sExpiryDate.second ) % 100

        return int('%d%d%06d%02d' % (t.tm_year, t.tm_yday, tCount, sCount))


    # 锁定新订单进行订单号占位
    def newSn(self):
        from models import Ord

        self.sn = self.getNewOrdSn()
        run = True

        while run:
            try:
                self.ord = Ord.objects.get(sn=self.sn)

            except:
                run = False

                self.ord = Ord.objects.create(sn=self.sn)

            else:
                self.sn += 1

        return self


    # 插入订单基本信息
    @subMsg(u'会员不存在，无法提交订单基本信息。')
    def pushOrd(self):
        from models import Ord

        Ord.objects.saveOrd(self.ord, self.request)
        return self


    # 物流信息提交
    @subMsg(u'无法提交物流信息。')
    def logcs(self):

        from logistics.models import Logcs

        Logcs.objects.saveLogcs(self.ord, self.request)

        return self


    # 商品信息提交
    @subMsg(u'部分商品已下架，无法提交商品信息。')
    def pro(self):
        from produce.models import Pro

        Pro.objects.savePro(self.ord, self.request)

        return self


    # 支付信息提交
    @subMsg(u'无法提交财务信息。')
    def fnc(self):
        from finance.models import Fnc

        Fnc.objects.saveFnc(self.ord, self.request)


        return self


    # 订单日志提交
    @subMsg(u'无法提交订单日志。')
    def log(self):
        from log.models import OrdLog

        OrdLog.objects.saveLog(self.ord, self.request)

        return self


    # 删除新订单
    def delNewOrd(self):
        self.ord.delete()

        return self


    # 订单提交完成
    @subMsg(u'订单提交无法完成。')
    def done(self):
        from cart.views import CartSess
        from logistics.views import LogcSess
        from finance.views import FncSess

        CartSess(self.request).clear()
        LogcSess(self.request).clear()
        OrdSess(self.request).clear()
        FncSess(self.request).clear()

        return self


    # 粗粒用户级错误提示
    def showError(self):
        messages.error(self.request, u'订单提交失败，请重新提交。')

        return rdrtBck(self.request)


    def editOrdFmt(self):
        from models import Ord

        self.sn = self.o['sn']

        self.ord = Ord.objects.get(sn=self.sn)

        self.ord.pro_set.all().delete()


        return self
