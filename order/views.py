#coding:utf-8
from django.shortcuts import render_to_response
from django.db.models import Q
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect
from new31.decorator import checkPOST, ordDetr, rdrBckDr, subFailRemind
from new31.func import forMatFee, rdrRange, page
from purview.views import BsPur
from decimal import Decimal
import time, datetime

# Create your views here.

# 订单列表显示页面
def ordList(request):
    from forms import OrdSrchFrm

    o = OrdSerch(request)

    form = OrdSrchFrm(initial=o.initial)

    oList = o.baseSearch().chcs().range().page()
    oList = OrdPur(oList, request).getOrds()

    return render_to_response('orderlist.htm', locals(), context_instance=RequestContext(request))


# 后台订单提交,提交成功后进行页面跳转至订单列表
@checkPOST
def submit(request):
    from logistics.views import Cnsgn
    Cnsgn(request).setSeesion()

    return OrdSub(request).submit().redirOrd()

# 后台新单编辑操作编辑页面
def newOrdUI(request):
    OrdSess(request).setStoZero()

    return editUI(request)

@ordDetr
def editOrd(request, c):
    o = OrdSess(request)
    o.cCon(request.GET.get('sn'), c)
    o.setSessBySN(request.GET.get('sn'))

    return HttpResponseRedirect(request.paths[u'编辑订单'])


# 后台订单编辑操作编辑页面@
def editUI(request):
    from cart.views import Cart
    from forms import ItemsForm, ordForm
    from logistics.forms import cnsgnForm
    from finance.forms import fncFrm

    items = Cart(request).showItemToCart()

    ItemsForm.getItemForms(items['items'])

    cnsgn = cnsgnForm(request)
    fnc = fncFrm(request)

    ord = ordForm(request)

    return render_to_response('orderneworedit.htm', locals(), context_instance=RequestContext(request))


def copyOrd(request,c):
    OrdSess(request).setSessBySN(int(request.GET.get('sn')))

    return HttpResponseRedirect(request.paths[u'新订单'])

@ordDetr
def cCon(request, c):
    OrdSess(request).cCon(request.GET.get('sn'), c)

    return rdrBck(request)



# 非新单及编辑以外的订单操作
def cCons(request, c):
    c = int(c)

    cons = [copyOrd, editOrd, cCon, cCon, cCon ]

    return cons[c](request, c)


# 后台订单编辑中添加商品至订单操作
@checkPOST
@rdrBckDr
def addItemToOrd(request, kwargs):
    from cart.views import Cart
    return Cart(request).pushToCartByItemIDs(request.POST.getlist('i'))


# 编辑界面中删除订单中的商品操作
@rdrBckDr
def delItemToOrd(request, kwargs):
    from cart.views import Cart

    return Cart(request).clearItemByMark(kwargs['mark'])


class OrdSess(object):
    """ 
        订单基本信息类

        存储于seesion数据的操作类

    """
    def __init__(self, request):
        from models import Ord
        # from django.contrib.auth.models import User
        self.request = request
        self.o = self.request.session.get('o')
        self.oFormat =  {
                        'typ': Ord.typs[0][0],
                        'status': Ord.chcs[0][0],
                        'sn': 0,
                        'user': self.request.user.username,
            }

    # 初始化seesion中用于存储订单的基本操作信息字典
    def format(self):
        if not self.o:
            return self.setSeesion(self.oFormat)

    def setSeesion(self, o):
        self.request.session['o'] = o

        return self

    def clear(self):

        return self.setSeesion(self.oFormat)

    def cCon(self, sn, c):
        order =  Ord.objects.get(sn=sn)

        order.status = c

        order.save()

        return self


    def setStoZero(self):

        self.o['status'] = 0

        return self


    def setStoOne(self):
        self.o['status'] = 1
        return self

    def cpyTsess(self, sn):
        order = Ord.objects.get(sn=sn)
        self.o['typ'] = order.typ
        self.o['sn'] = sn

        return self.setStoOne()

    def cpyCongn(self, sn):
        from consignee.views import Cnsgn
        sCongn = Cnsgn(self.request)
        c = sCongn.cFormat.copy()

        oLogcs = Ord.objects.get(sn=sn).logcs
 
        areaList = oLogcs.area.split(' - ')


        try:
            area = Area.objects.get(name=areaList[1]).id
        except Exception, e:
            area = Area.objects.getDefault().id


        try:
            time = SignTime.objects.get(start=oLogcs.stime, end=oLogcs.etime).id
        except Exception, e:
            time = SignTime.objects.getDefault().id

        c['user'] = oLogcs.ord.user
        c['pay'] = oLogcs.ord.fnc.cod.id
        c['consignee'] = oLogcs.consignee
        c['area'] = area
        c['address'] = oLogcs.address
        c['tel'] = oLogcs.tel
        c['date'] = '%s' % oLogcs.date

        c['time'] = time
        c['note'] = oLogcs.note

        sCongn.setConsignee(c)


        return self

    def cpyItem(self, sn):
        from cart.views import Cart
        from discount.models import Dis
        c = Cart(self.request).clear()

        order = Ord.objects.get(sn=sn)
        items = order.orditem_set.all()
        _items = []

        for i in items:
            ii = ItemSpec.objects.get(item__name=i.name, spec__value=i.spec)

            item = c.item.copy()
            item['itemID'] = ii.item.id
            item['specID'] = ii.id
            item['disID'] = Dis.objects.get(dis=i.dis).id
            item['num'] = i.num

            _items.append(item)

        c.pushItem(_items)

        return self


    # 将订单信息配置到seesion当
    def setSessBySN(self, sn):

        return self.cpyTsess(sn).cpyCongn(sn).cpyItem(sn)


    def stopOrd(self, sn):

        return self.cCon(sn, 4)



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

    def chcs(self):
            if self.initial['c'] >= 0:
                self.oList = self.oList.filter(status=self.initial['c'])

            return self

    def range(self):

        self.oList = self.oList.filter((Q(ordlog__typ=0) | Q(ordlog__typ=1)), ordlog__time__range=(self.initial['s'], self.initial['e']) )

        return self

    def page(self):

        return page(l=self.oList, p=int(self.request.GET.get('p', 1)))


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
        self.path = request.paths[u'订单']

        self.chcs = Ord.chcs
        self.action = Ord.act


    # 获取订单可选操作项
    def getElement(self):

        for i in self.oList:
            if not hasattr(i,'action'):
                i.action = {}

            i.action[self.path] = self.action[i.status]

        return self


class OrdSub(object):
    """ 
        订单提交类.

        订单提交只需实例后, 使用 <<submit>> 方法即可
        示例: OrdSubmit(request).submit()

        订单数据来源为session中数据

        session['items'] = 商品信息
        session['c'] = 联系人信息
        session['o'] = 订单基本信息, 比如订单类型, 新单或编辑



        此类已根据 setting.DEBUG 对类方法进行了 <<用户级提示>> 装饰
        当 settings.DEBUG = True 时, 用户级提示关闭, 反之开启.

    """
    def __init__(self, request):
        self.request = request
        self.error = False

        self.o = OrdSess(self.request).o


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

        # 异常时对数据库进行处理
        if self.error:
            self.delNewOrd()

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
    @subFailRemind(u'会员不存在，无法提交订单基本信息。')
    def pushOrd(self):
        from models import Ord

        Ord.objects.saveOrd(self.ord, self.request)
        return self


    # 物流信息提交
    @subFailRemind(u'无法提交物流信息。')
    def logcs(self):

        from logistics.models import Logcs

        Logcs.objects.saveLogcs(self.ord, self.request)

        return self


    # 商品信息提交
    @subFailRemind(u'部分商品已下架，无法提交商品信息。')
    def pro(self):
        from produce.models import Pro

        Pro.objects.savePro(self.ord, self.request)

        return self

    # 支付信息提交
    @subFailRemind(u'无法提交财务信息。')
    def fnc(self):
        from finance.models import Fnc

        Fnc.objects.saveFnc(self.ord, self.request)


        return self



    # 订单日志提交
    @subFailRemind(u'无法提交订单日志。')
    def log(self):
        from log.models import OrdLog

        OrdLog.objects.saveLog(self.ord, self.request)

        return self


    # 删除新订单
    def delNewOrd(self):
        self.ord.delete()

        return self


    # 订单提交完成
    @subFailRemind(u'订单提交无法完成。')
    def done(self):
        from cart.views import Cart
        from logistics.views import Cnsgn
        from finance.views import FncSess

        Cart(self.request).clear()
        Cnsgn(self.request).clear()
        OrdSess(self.request).clear()
        FncSess(self.request).clear()

        return self


    # 显示订单号,主要用于前提用户级提示
    def showOrdSN(self):
        if self.error:
            return self.showError()
        else:
            messages.success(self.request, u'您已成功提交订单!')
            messages.success(self.request, u'感谢您在本店购物！请记住您的订单号: %s' % self.sn)

            return HttpResponseRedirect('/')


    # 重定向至订单列表页
    def redirOrd(self):
        from logistics.views import Cnsgn
        if self.error:
            return self.showError()
        else:
            messages.success(self.request, u'订单提交成功: %s' % self.sn)

            return rdrRange(self.request.paths[u'订单'], Cnsgn(self.request).c['date'], self.sn)

    # 粗粒用户级错误提示
    def showError(self):
        messages.error(self.request, u'订单提交失败，请重新提交。')

        return rdrBck(self.request)


    def editOrdFmt(self):

        self.sn = self.o['sn']

        self.ord = Ord.objects.get(sn=self.sn)

        self.logcs = self.ord.logcs
        self.oPay = self.ord.fnc
        self.oStart = self.ord
        self.oShip = self.ord.ordship
        self.oOLT = self.ord.ordlog_set.get(Q(log=0) | Q(log=1))


        self.ord.orditem_set.all().delete()



        return self
