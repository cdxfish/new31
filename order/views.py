#coding:utf-8
from django.shortcuts import render_to_response
from django.db.models import Q
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect
from new31.decorator import postDr, rdrtBckDr
from cart.decorator import checkCartDr
from new31.func import frMtFee, rdrRange, page, rdrtBck
from decorator import ordDr, subMsg, subDr
from logistics.decorator import chLogcsDr
from finance.decorator import chFncDr
from decimal import Decimal
import time, datetime

# Create your views here.

# 订单列表显示页面
def ordList(request):
    from forms import OrdSrchFrm

    o = OrdSerch(request)
    oList = o.get()
    oList = OrdPur(oList, request).get()

    form = OrdSrchFrm(initial=o.initial)

    return render_to_response('orderlist.htm', locals(), context_instance=RequestContext(request))


# 后台订单提交,提交成功后进行页面跳转至订单列表
@postDr
@checkCartDr
@chLogcsDr
@chFncDr
@subDr
def submit(request):
    from logistics.views import LogcSess

    logcs = LogcSess(request).setByDict(request.POST.dict())

    o = OrdSub(request).submit()

    if o.error:
        return o.showError()
    else:
        messages.success(request, u'订单提交成功: %s' % o.sn)

        return rdrRange(request.pPath[u'订单'], logcs.sess['date'], o.sn)


# 后台新单编辑操作编辑页面
def newOrdUI(request):
    OrdSess(request).setSzero()

    return editUI(request)

@ordDr
def editOrd(request, s):
    from models import Ord
    Ord.objects.cStatus(request.GET.get('sn'), s)

    OrdSess(request).copy(request.GET.get('sn'))

    return HttpResponseRedirect(request.pPath[u'编辑订单'])


# 后台订单编辑操作编辑页面@
def editUI(request):
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


def copyOrd(request,c):
    OrdSess(request).copy(int(request.GET.get('sn')))

    return HttpResponseRedirect(request.pPath[u'新订单'])

@ordDr
def cCon(request, s):
    from models import Ord
    Ord.objects.cStatus(request.GET.get('sn'), s)

    return rdrtBck(request)


# 非新单及编辑以外的订单操作
def cCons(request, s):
    s = int(s)

    cons = [copyOrd, editOrd, cCon, cCon, cCon ]

    return cons[s](request, s)


# 后台订单编辑中添加商品至订单操作
@postDr
@rdrtBckDr('无法添加商品，部分商品已下架。')
def addItem(request):
    from cart.views import CartSess

    CartSess(request).pushByIDs(request.POST.getlist('i'))
    return rdrtBck(request)


# 编辑界面中删除订单中的商品操作
@rdrtBckDr('无法删除商品，请与管理员联系。')
def delItem(request):
    from cart.views import CartSess

    CartSess(request).delete(int(request.GET.get('mark')))

    return rdrtBck(request)


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

        return self.cpyOrd(sn).cpyLogcs(sn).cpyItem(sn)


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
                        'k': request.GET.get('k', '').strip(), 
            }

        
    def baseSearch(self):

        q = (
                Q(sn__contains=self.initial['k']) |
                Q(user__username__contains=self.initial['k']) |
                Q(logcs__consignee__contains=self.initial['k']) |
                Q(logcs__area__contains=self.initial['k']) |
                Q(logcs__address__contains=self.initial['k']) |
                Q(logcs__tel__contains=self.initial['k']) |
                # Q(logcs__date=datetime.date.today()) |
                Q(logcs__stime__contains=self.initial['k']) |
                Q(logcs__etime__contains=self.initial['k']) |
                Q(logcs__note__contains=self.initial['k'])
            )

        self.oList = self.oList.filter(q)

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

        self.oList = self.oList.filter((Q(ordlog__typ=0) | Q(ordlog__typ=1)), ordlog__time__range=(self.initial['s'], self.initial['e']) )

        return self

    def page(self):

        return page(l=self.oList, p=int(self.request.GET.get('p', 1)))

    def get(self):

        return self.baseSearch().search().chcs().range().page()


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
        self.path = request.pPath[u'订单']

        self.chcs = Ord.chcs
        self.action = Ord.act


    # 获取订单可选操作项
    def getElement(self):

        for i in self.oList:
            if not hasattr(i,'action'):
                i.action = {}

            i.action[self.path] = self.action[i.status]
            i.optr = 'sn'
            i.value = i.sn

        return self


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
        # self.newSn()

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
