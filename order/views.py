#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib import messages, auth
from django.db.models import Q
from new31.decorator import *
from new31.func import *
from signtime.models import *
from area.models import *
from item.models import *
from payment.models import *
from models import *
from forms import *
from decimal import *
from consignee.forms import *
from purview.views import *
import time, datetime

# Create your views here.

# 订单列表显示页面
def ordList(request):
    o = OrdSerch(request)

    form = OrdSatsForm(initial=o.initial)

    oList = o.baseSearch().chcs().range().page()
    oList = OrdPur(oList, request).getOrds()

    return render_to_response('orderlist.htm', locals(), context_instance=RequestContext(request))


# 后台订单提交,提交成功后进行页面跳转至订单列表
@checkPOST
def submit(request):
    from consignee.views import SpCnsgn
    SpCnsgn(request).setSeesion()

    return OrdSub(request).submit().redirOrd()

# 后台新单编辑操作编辑页面
def newOrdUI(request):
    Ord(request).setStoZero()

    return editUI(request)

@ordDetr
def editOrd(request, c):
    o = Ord(request)
    o.cCon(request.GET.get('sn'), c)
    o.setSessBySN(request.GET.get('sn'))

    return HttpResponseRedirect(request.paths[u'编辑订单'])


# 后台订单编辑操作编辑页面@
def editUI(request):
    from cart.views import Cart

    items = Cart(request).showItemToCart()

    ItemsForm.getItemForms(items['items'])

    form = conFrm(request)

    oTypeForm = getOTpyeForm(request)

    return render_to_response('orderneworedit.htm', locals(), context_instance=RequestContext(request))


def copyOrd(request,c):
    Ord(request).setSessBySN(int(request.GET.get('sn')))

    return HttpResponseRedirect(request.paths[u'新订单'])

@ordDetr
def cCon(request, c):
    Ord(request).cCon(request.GET.get('sn'), c)

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


class Ord(object):
    """ 
        订单基本信息类

        存储于seesion数据的操作类

    """
    def __init__(self, request):
        self.request = request
        self.o = self.request.session.get('o')
        self.oFormat =  {
                        'typ': OrdInfo.chcs[0][0],
                        'status': OrdSats.chcs[0][0],
                        'sn': 0,
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
        order =  OrdInfo.objects.get(sn=sn).ordsats

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
        order = OrdInfo.objects.get(sn=sn)
        self.o['typ'] = order.typ
        self.o['sn'] = sn

        return self.setStoOne()

    def cpyCongn(self, sn):
        from consignee.views import SpCnsgn
        sCongn = SpCnsgn(self.request)
        c = sCongn.cFormat.copy()

        oLogcs = OrdInfo.objects.get(sn=sn).ordlogcs
 
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
        c['pay'] = oLogcs.ord.ordpay.cod.id
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
        from discount.models import Discount
        c = Cart(self.request).clear()

        order = OrdInfo.objects.get(sn=sn)
        items = order.orditem_set.all()
        _items = []

        for i in items:
            ii = ItemSpec.objects.get(item__name=i.name, spec__value=i.spec)

            item = c.item.copy()
            item['itemID'] = ii.item.id
            item['specID'] = ii.id
            item['disID'] = Discount.objects.get(dis=i.dis).id
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
        self.request = request

        self.oList = OrdInfo.objects.select_related().all()

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
                Q(ordlogcs__consignee__contains=self.initial['k']) |
                Q(ordlogcs__area__contains=self.initial['k']) |
                Q(ordlogcs__address__contains=self.initial['k']) |
                Q(ordlogcs__tel__contains=self.initial['k']) |
                # Q(ordlogcs__date=datetime.date.today()) |
                Q(ordlogcs__stime__contains=self.initial['k']) |
                Q(ordlogcs__etime__contains=self.initial['k']) |
                Q(ordlogcs__note__contains=self.initial['k'])
            )

        self.oList = self.oList.filter(q)

        if self.initial['o'] >= 0:
            self.oList = self.oList.filter(typ=self.initial['o'])

        return self

    def chcs(self):
            if self.initial['c'] >= 0:
                self.oList = self.oList.filter(ordsats__status=self.initial['c'])

            return self

    def range(self):

        self.oList = self.oList.filter((Q(ordlog__log=0) | Q(ordlog__log=1)), ordlog__time__range=(self.initial['s'], self.initial['e']) )

        return self

    def page(self):

        return page(l=self.oList, p=int(self.request.GET.get('p', 1)))


class OrdPur(OrdPur):
    """
        订单列表权限加持

        获取当前角色可进行的订单操作权限.
        获取订单状态,判定可选权限.
        两者进行交集操作.

    """

    def __init__(self, oList, request):
        super(OrdPur, self).__init__(oList, request)
        self.path = request.paths[u'订单']

        order =  OrdSats
        self.chcs = order.chcs
        self.action = order.act


    # 获取订单可选操作项
    def getElement(self):

        for i in self.oList:
            if not hasattr(i,'action'):
                i.action = {}

            i.action[self.path] = self.action[i.ordsats.status]

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
        from cart.views import Cart
        self.items = Cart(self.request).items
        from consignee.views import SpCnsgn
        self.c = SpCnsgn(self.request).c
        self.o = Ord(self.request).o
        self.logcs = OrdLogcs()
        self.oPay = OrdPay()
        self.oStart = OrdSats()
        self.oShip = OrdShip()
        self.oOLT = OrdLog()

    def submit(self):

        if self.o['status']:
            self.editOrdFmt()

        else:
            self.newSn()

        self.infoSubmit()
        self.logcsSub()
        self.itemSub()
        self.paySub()
        self.shipSub()
        self.oSatSub()
        self.logSub()
        self.subDone()

        # 异常时对数据库进行处理
        # if self.error:
        #     self.delNewOrd()

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
        self.sn = self.getNewOrdSn()

        run = True

        while run:
            try:
                self.ord = OrdInfo.objects.get(sn=self.sn)

            except:
                run = False

                self.ord = OrdInfo.objects.create(sn=self.sn)

            else:
                self.sn += 1

        return self


    # 插入订单基本信息
    @subFailRemind(u'会员不存在，无法提交订单基本信息。')
    def infoSubmit(self):
        if self.c['user']:
            self.ord.user= auth.models.User.objects.get(username=self.c['user'])

        self.ord.typ = self.o['typ']
        self.ord.save()

        return self


    # 物流信息提交
    @subFailRemind(u'无法提交物流信息。')
    def logcsSub(self):

        logisticsTimeAvdce = 1 # 默认偏移1hour

        time = SignTime.objects.get(id=self.c['time'], onl=True)

        area = Area.objects.get(id= self.c['area'], onl=True)

        self.logcs.consignee = self.c['consignee']
        self.logcs.area = '%s - %s' % (area.sub.name, area.name)
        self.logcs.address = self.c['address']
        self.logcs.tel = self.c['tel']
        self.logcs.date = self.c['date']
        self.logcs.stime = time.start
        self.logcs.etime = time.end
        self.logcs.lstime = time.start.replace(hour = time.start.hour - logisticsTimeAvdce)
        self.logcs.letime = time.end.replace(hour = time.end.hour - logisticsTimeAvdce)
        self.logcs.note = self.c['note']

        self.logcs.ord = self.ord

        self.logcs.save()

        return self


    # 商品信息提交
    @subFailRemind(u'部分商品已下架，无法提交商品信息。')
    def itemSub(self):

        items = []

        for v,i in self.items.items():

            item = Item.objects.getItemByItemID(id=i['itemID'])
            spec = ItemSpec.objects.getSpecBySpecID(id=i['specID']).spec
            fee = ItemFee.objects.getFeeBySpecID(id=i['specID'])
            dis = Discount.objects.getDisByDisID(id=i['disID'])
            nfee = forMatFee(fee.fee * Decimal(dis.dis))

            items.append(
                OrdItem(
                    ord=self.ord,
                    name=item.name,
                    sn=item.sn,
                    spec=spec.value,
                    num=i['num'],
                    fee=fee.fee,
                    dis=dis.dis,
                    nfee=nfee
                    )
                )

        OrdItem.objects.bulk_create(items)

        return self

    # 支付信息提交
    @subFailRemind(u'无法提交支付信息提交。')
    def paySub(self):

        pay = Pay.objects.getPayById(id=self.c['pay'])

        self.oPay.ord = self.ord
        self.oPay.cod = pay

        self.oPay.save()

        return self


    # 配送方式信息提交
    @subFailRemind(u'无法提交配送方式信息。')
    def shipSub(self):

        # ship = Pay.objects.getPayById(id=self.c['ship'])

        self.oShip.ord = self.ord
        # self.oShip.name = ship.name
        # self.oShip.cod = ship.cod

        self.oShip.name = u'市内免费送货上门'
        self.oShip.cod = u'fditc'

        self.oShip.save()

        return self


    # 订单状态提交
    @subFailRemind(u'无法提订单状态。')
    def oSatSub(self):

        self.oStart.ord = self.ord

        self.oStart.save()

        return self


    # 订单日志提交
    @subFailRemind(u'无法提交订单日志。')
    def logSub(self):

        self.oOLT.ord = self.ord
        self.oOLT.user = self.request.user
        if self.o['status']:
            self.oOLT.log = 1

        self.oOLT.save()

        return self


    # 删除新订单
    def delNewOrd(self):
        self.ord.delete()

        return self


    # 订单提交完成
    @subFailRemind(u'订单提交无法完成。')
    def subDone(self):
        from cart.views import Cart
        Cart(self.request).clear()
        from consignee.views import SpCnsgn
        SpCnsgn(self.request).clear()
        Ord(self.request).clear()


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
        if self.error:
            return self.showError()
        else:
            messages.success(self.request, u'订单提交成功: %s' % self.sn)

            return rdrRange(self.request.paths[u'订单'], self.c['date'], self.sn)

    # 粗粒用户级错误提示
    def showError(self):
        messages.error(self.request, u'订单提交失败，请重新提交。')

        return rdrBck(self.request)


    def editOrdFmt(self):

        self.sn = self.o['sn']

        self.ord = OrdInfo.objects.get(sn=self.sn)

        self.logcs = self.ord.ordlogcs
        self.oPay = self.ord.ordpay
        self.oStart = self.ord.ordsats
        self.oShip = self.ord.ordship
        self.oOLT = self.ord.ordlog_set.get(Q(log=0) | Q(log=1))


        self.ord.orditem_set.all().delete()



        return self
