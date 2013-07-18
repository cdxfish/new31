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
def orderList(request):
    o = OrderSerch(request)

    form = OrderStatusForm(initial=o.initial)

    oList = o.baseSearch().chcs().range().page()
    oList = OrdPur(oList, request).getOrders()

    return render_to_response('orderlist.htm', locals(), context_instance=RequestContext(request))


# 后台订单提交,提交成功后进行页面跳转至订单列表
@checkPOST
def submit(request):
    from consignee.views import ShipConsignee
    ShipConsignee(request).setSeesion()

    return OrdSub(request).submit().redirOrder()

# 后台新单编辑操作编辑页面
def newOrderUI(request):
    Order(request).setStoZero()

    return editUI(request)

@conOrder
def editOrd(request, c):
    o = Order(request)
    o.cCon(request.GET.get('sn'), c)
    o.setSessBySN(request.GET.get('sn'))

    return HttpResponseRedirect(request.paths[u'编辑订单'])


# 后台订单编辑操作编辑页面
@ordImps
def editUI(request):
    from cart.views import Cart

    items = Cart(request).showItemToCart()

    ItemsForm.getItemForms(items['items'])

    form = getForms(request)

    oTypeForm = getOTpyeForm(request)

    return render_to_response('orderneworedit.htm', locals(), context_instance=RequestContext(request))


def copyOrder(request,c):
    Order(request).setSessBySN(int(request.GET.get('sn')))

    return HttpResponseRedirect(request.paths[u'新订单'])

@conOrder
def cCon(request, c):
    Order(request).cCon(request.GET.get('sn'), c)

    return redirectBack(request)



# 非新单及编辑以外的订单操作
def cCons(request, c):
    c = int(c)

    cons = [copyOrder, editOrd, cCon, cCon, cCon ]

    return cons[c](request, c)


# 后台订单编辑中添加商品至订单操作
@checkPOST
@decoratorBack
def addItemToOrder(request, kwargs):
    from cart.views import Cart
    return Cart(request).pushToCartByItemIDs(request.POST.getlist('i'))


# 编辑界面中删除订单中的商品操作
@decoratorBack
def delItemToOrder(request, kwargs):
    from cart.views import Cart

    return Cart(request).clearItemByMark(kwargs['mark'])


class Order(object):
    """ 
        订单基本信息类

        存储于seesion数据的操作类

    """
    def __init__(self, request):
        self.request = request
        self.o = self.request.session.get('o')
        self.oFormat =  {
                        'typ': OrderInfo.chcs[0][0],
                        'status': OrderStatus.chcs[0][0],
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
        order =  OrderInfo.objects.get(sn=sn).orderstatus
        act = OrderStatus.objects.getActTuple(order.status)

        if not c in act:

            messages.error(self.request, u'%s - 无法%s' % (sn, order.get_status_display()))

            return redirectBack(self.request)

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
        order = OrderInfo.objects.get(sn=sn)
        self.o['typ'] = order.typ
        self.o['sn'] = sn

        return self.setStoOne()

    def cpyCongn(self, sn):
        from consignee.views import ShipConsignee
        sCongn = ShipConsignee(self.request)
        c = sCongn.cFormat.copy()

        oLogistics = OrderInfo.objects.get(sn=sn).orderlogistics

        orderPay = oLogistics.order.orderpay

        try:
            pay = Pay.objects.get(name=orderPay.payName, cod=orderPay.cod).id
        except Exception, e:
            pay = Pay.objects.getDefault().id

        areaList = oLogistics.area.split(' - ')


        try:
            area = Area.objects.get(name=areaList[1]).id
        except Exception, e:
            area = Area.objects.getDefault().id


        try:
            time = SignTime.objects.get(signTimeStart=oLogistics.start, signTimeEnd=oLogistics.end).id
        except Exception, e:
            time = SignTime.objects.getDefault().id

        c['user'] = oLogistics.order.user
        c['pay'] = pay
        c['consignee'] = oLogistics.consignee
        c['area'] = area
        c['address'] = oLogistics.address
        c['tel'] = oLogistics.tel
        c['signDate'] = '%s' % oLogistics.signDate

        c['time'] = time
        c['note'] = oLogistics.note

        sCongn.setConsignee(c)


        return self

    def cpyItem(self, sn):
        from cart.views import Cart
        from discount.models import Discount
        c = Cart(self.request).clear()

        order = OrderInfo.objects.get(sn=sn)
        items = order.orderitem_set.all()
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



class OrderSerch(object):
    """
        订单基本搜索类

    """
    def __init__(self, request):
        self.request = request

        self.oList = OrderInfo.objects.select_related().all()

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
                Q(orderlogistics__consignee__contains=self.initial['k']) |
                Q(orderlogistics__area__contains=self.initial['k']) |
                Q(orderlogistics__address__contains=self.initial['k']) |
                Q(orderlogistics__tel__contains=self.initial['k']) |
                # Q(orderlogistics__signDate=datetime.date.today()) |
                Q(orderlogistics__signTimeStart__contains=self.initial['k']) |
                Q(orderlogistics__signTimeEnd__contains=self.initial['k']) |
                Q(orderlogistics__note__contains=self.initial['k'])
            )

        self.oList = self.oList.filter(q)

        if self.initial['o'] >= 0:
            self.oList = self.oList.filter(typ=self.initial['o'])

        return self

    def chcs(self):
            if self.initial['c'] >= 0:
                self.oList = self.oList.filter(orderstatus__status=self.initial['c'])

            return self

    def range(self):

        self.oList = self.oList.filter((Q(orderlog__log=0) | Q(orderlog__log=1)), orderlog__time__range=(self.initial['s'], self.initial['e']) )

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
        self.chcs = OrderStatus.chcs
        self.path = request.paths[u'订单']
        self.action = OrderStatus.act


    # 获取订单可选操作项
    def getElement(self):

        for i in self.oList:
            if not hasattr(i,'action'):
                i.action = {}

            i.action[self.path] = self.action[i.orderstatus.status]

        return self


class OrdSub(object):
    """ 
        订单提交类.

        订单提交只需实例后, 使用 <<submit>> 方法即可
        示例: OrderSubmit(request).submit()

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
        from consignee.views import ShipConsignee
        self.c = ShipConsignee(self.request).c
        self.o = Order(self.request).o
        self.logcs = OrderLogistics()
        self.oPay = OrderPay()
        self.oStart = OrderStatus()
        self.oShip = OrderShip()
        self.oOLT = OrderLog()

    def submit(self):

        if self.o['status']:
            self.editOrdFmt()

        else:
            self.newOderSn()

        self.infoSubmit()
        self.logisticsSubmit()
        self.itemSubmit()
        self.paySubmit()
        self.shipSubmit()
        self.oStartSubmit()
        self.oLogSubmit()
        self.submitDone()

        # 异常时对数据库进行处理
        # if self.error:
        #     self.delNewOrder()

        return self

    # 获得新的订单编号
    def getNewOrderSn(self):
        t = time.gmtime()
        tCount = int('%02d%02d%02d' % (t.tm_hour,t.tm_min, t.tm_sec))
        sExpiryDate = self.request.session.get_expiry_date()
        sCount = (sExpiryDate.hour * sExpiryDate.minute * sExpiryDate.second ) % 100

        return int('%d%d%06d%02d' % (t.tm_year, t.tm_yday, tCount, sCount))


    # 锁定新订单进行订单号占位
    def newOderSn(self):
        self.sn = self.getNewOrderSn()

        run = True

        while run:
            try:
                self.order = OrderInfo.objects.get(sn=self.sn)

            except:
                run = False

                self.order = OrderInfo.objects.create(sn=self.sn)

            else:
                self.sn += 1

        return self


    # 插入订单基本信息
    @subFailRemind(u'会员不存在，无法提交订单基本信息。')
    def infoSubmit(self):
        if self.c['user']:
            self.order.user= auth.models.User.objects.get(username=self.c['user'])

        self.order.typ = self.o['typ']
        self.order.save()

        return self


    # 物流信息提交
    @subFailRemind(u'无法提交物流信息。')
    def logisticsSubmit(self):

        logisticsTimeAvdce = 1 # 默认偏移1hour

        time = SignTime.objects.get(id=self.c['time'], onl=True)

        area = Area.objects.get(id= self.c['area'], onl=True)

        self.logcs.consignee = self.c['consignee']
        self.logcs.area = '%s - %s' % (area.sub.name, area.name)
        self.logcs.address = self.c['address']
        self.logcs.tel = self.c['tel']
        self.logcs.signDate = self.c['signDate']
        self.logcs.signTimeStart = time.start
        self.logcs.signTimeEnd = time.end
        self.logcs.logisTimeStart = time.start.replace(hour = time.start.hour - logisticsTimeAvdce)
        self.logcs.logisTimeEnd = time.end.replace(hour = time.end.hour - logisticsTimeAvdce)
        self.logcs.note = self.c['note']

        self.logcs.order = self.order

        self.logcs.save()

        return self


    # 商品信息提交
    @subFailRemind(u'部分商品已下架，无法提交商品信息。')
    def itemSubmit(self):

        items = []

        for v,i in self.items.items():

            item = Item.objects.getItemByItemID(id=i['itemID'])
            spec = ItemSpec.objects.getSpecBySpecID(id=i['specID']).spec
            fee = ItemFee.objects.getFeeBySpecID(id=i['specID'])
            dis = Discount.objects.getDisByDisID(id=i['disID'])
            nfee = forMatFee(fee.fee * Decimal(dis.dis))

            items.append(
                OrderItem(
                    order=self.order,
                    name=item.name,
                    sn=item.sn,
                    spec=spec.value,
                    num=i['num'],
                    fee=fee.fee,
                    dis=dis.dis,
                    nfee=nfee
                    )
                )

        OrderItem.objects.bulk_create(items)

        return self

    # 支付信息提交
    @subFailRemind(u'无法提交支付信息提交。')
    def paySubmit(self):

        pay = Pay.objects.getPayById(id=self.c['pay'])

        self.oPay.order = self.order
        self.oPay.name = pay.name
        self.oPay.cod = pay.cod

        self.oPay.save()

        return self


    # 配送方式信息提交
    @subFailRemind(u'无法提交配送方式信息。')
    def shipSubmit(self):

        # ship = Pay.objects.getPayById(id=self.c['ship'])

        self.oShip.order = self.order
        # self.oShip.name = ship.name
        # self.oShip.cod = ship.cod

        self.oShip.name = u'市内免费送货上门'
        self.oShip.cod = u'fditc'

        self.oShip.save()

        return self


    # 订单状态提交
    @subFailRemind(u'无法提订单状态。')
    def oStartSubmit(self):

        self.oStart.order = self.order

        self.oStart.save()

        return self


    # 订单日志提交
    @subFailRemind(u'无法提交订单日志。')
    def oLogSubmit(self):

        self.oOLT.order = self.order
        self.oOLT.user = self.request.user
        if self.o['status']:
            self.oOLT.log = 1

        self.oOLT.save()

        return self


    # 删除新订单
    def delNewOrder(self):
        self.order.delete()

        return self


    # 订单提交完成
    @subFailRemind(u'订单提交无法完成。')
    def submitDone(self):
        from cart.views import Cart
        Cart(self.request).clear()
        from consignee.views import ShipConsignee
        ShipConsignee(self.request).clear()
        Order(self.request).clear()


        return self


    # 显示订单号,主要用于前提用户级提示
    def showOrderSN(self):
        if self.error:
            return self.showError()
        else:
            messages.success(self.request, u'您已成功提交订单!')
            messages.success(self.request, u'感谢您在本店购物！请记住您的订单号: %s' % self.sn)

            return HttpResponseRedirect('/')


    # 重定向至订单列表页
    def redirOrder(self):
        if self.error:
            return self.showError()
        else:
            messages.success(self.request, u'订单提交成功: %s' % self.sn)
            d = datetime.datetime.strptime(self.c['signDate'], "%Y-%m-%d")
            s = d - datetime.timedelta(days=1)
            e = d + datetime.timedelta(days=1)

            return HttpResponseRedirect(u'/order/?o=-1&c=-1&s=%s&e=%s&k=%s' % (s.strftime('%Y-%m-%d').strip(), e.strftime('%Y-%m-%d').strip(), self.sn))


    # 粗粒用户级错误提示
    def showError(self):
        messages.error(self.request, u'订单提交失败，请重新提交。')

        return redirectBack(self.request)


    def editOrdFmt(self):

        self.sn = self.o['sn']

        self.order = OrderInfo.objects.get(sn=self.sn)

        self.logcs = self.order.orderlogistics
        self.oPay = self.order.orderpay
        self.oStart = self.order.orderstatus
        self.oShip = self.order.ordership
        self.oOLT = self.order.orderlog_set.get(Q(log=0) | Q(log=1))


        self.order.orderitem_set.all().delete()



        return self
