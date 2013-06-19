#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from new31.decorator import *
from new31.func import *
from signtime.models import *
from cart.views import *
from area.models import *
from item.models import *
from payment.models import *
from models import *
from forms import *
from decimal import *
from consignee.forms import *
import time, json
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.

# 订单列表显示页面
def orderList(request):

    form = getOstatusForm(request)

    oList = Order(request).oList()

    oList = OrderListPurview(oList, request).getElement().beMixed()

    return render_to_response('orderlist.htm', locals(), context_instance=RequestContext(request))


# 订单信息编辑提交
def cCon(request, c):

    c = int(c)
    orderSN = request.GET.get('sn')
    order =  OrderInfo.objects.get(orderSn=orderSN).orderstatus

    order.orderStatus = c

    order.save()

    if not c == 2:
        return HttpResponseRedirect('/order/')

    else:
        # 将订单信息配置到seesion当中
        ShipConsignee(request).setSiessionByOrder(sn=orderSN)
        Order(request).setSeesion(OrderInfo.objects.get(orderSn=orderSN).orderType)

        return HttpResponseRedirect('/order/new/')


# 前台订单提交,并是用前台消息模板显示订单号等信息
@checkPOST
def carSub(request):

    return OrderSubmit(request).submit().showOrderSN()


# 后台订单提交,提交成功后进行页面跳转至订单列表
@checkPOST
def adminSub(request):

    ShipConsignee(request).setSeesion()

    return OrderSubmit(request).submit().redirOrder()


# 后台新单及订单编辑操作编辑页面
def newOrEditOrderUI(request):
    items = Cart(request).showItemToCart()

    form = getForms(request)

    oTypeForm = getOTpyeForm(request)

    return render_to_response('orderneworedit.htm', locals(), context_instance=RequestContext(request))


# 后台订单编辑中添加商品至订单操作
@checkPOST
@decoratorBack
def addItemToOrder(request, kwargs):

    return Cart(request).pushToCartByItemIDs(request.POST.getlist('i'))


# 编辑界面中删除订单中的商品操作
@decoratorBack
def delItemToOrder(request, kwargs):

    return Cart(request).clearItemByMark(kwargs['mark'])


class Order:
    """ 订单基本信息类

        存储于seesion数据的操作类

    """
    def __init__(self, request):
        self.request = request
        self.oType = request.session.get('oType')
        self.oFormat = OrderInfo.oType[0][0]
        
    def format(self):
        if not self.oType:
            return self.setSeesion(self.oFormat)

    def setSeesion(self, oType):
        self.request.session['oType'] = oType

        return self

    def clear(self):

        return self.setSeesion(self.oFormat)

    def oList(self):

        s = self.request.GET.get('s', '%s' % datetime.date.today())
        e = self.request.GET.get('e', '%s' % datetime.date.today())
        k = self.request.GET.get('k', '').strip()

        o = int(self.request.GET.get('o', -1))
        c = int(self.request.GET.get('c', 0))
        p = int(self.request.GET.get('p', 1))

        q = (
                Q(orderSn__contains=k) | 
                # Q(user__contains=k) | 
                Q(orderlogistics__consignee__contains=k)
            )

        oList = OrderInfo.objects.select_related().filter(q)

        if o >= 0:
            oList = oList.filter(orderType=o)

        if c >= 0:
            oList = oList.filter(orderstatus__orderStatus=c)

        oList = oList.filter(orderlog__time__range=(s, e), orderlog__log=0)


        return page(l=oList, p=p)


class OrderSubmit:
    """ 订单提交类.

        订单提交只需实例后, 使用 <<submit>> 方法即可
        示例: OrderSubmit(request).submit()

        订单数据来源为session中数据

        session['items'] = 商品信息
        session['oType'] = 订单类型
        session['c'] = 联系人信息



        此类已根据 setting.DEBUG 对类方法进行了 <<用户级提示>> 装饰
        当 settings.DEBUG = True 时, 用户级提示关闭, 反之开启.

    """
    def __init__(self, request):
        self.request = request
        self.error = False

        self.items = Cart(self.request).items
        self.c = ShipConsignee(self.request).c


    def submit(self):

        self.newOderSn() \
            .infoSubmit() \
            .logisticsSubmit() \
            .itemSubmit() \
            .paySubmit() \
            .shipSubmit() \
            .oStartSubmit() \
            .oLogSubmit() \
            .submitDone()

        # 异常时对数据库进行处理
        if self.error:
            self.delNewOrder()

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
        self.orderId = self.getNewOrderSn()

        run = True

        while run:
            try:
                self.order = OrderInfo.objects.get(orderSn=self.orderId)

            except:
                run = False

                self.order = OrderInfo.objects.create(orderSn=self.orderId)

            else:
                self.orderId += 1

        return self


    # 插入订单基本信息
    @subFailRemind('会员不存在，无法提交订单基本信息。')
    def infoSubmit(self):
        if self.c['user']:
            self.order.user= User.objects.get(username=self.c['user'])

        self.order.orderType = Order(self.request).oType
        self.order.save()

        return self


    # 物流信息提交
    @subFailRemind('无法提交物流信息。')
    def logisticsSubmit(self):

        logisticsTimeAvdce = 1

        time = SignTime.objects.get(id=self.c['time'], onLine=True)

        area = Area.objects.get(id= self.c['area'], onLine=True)

        logistics = OrderLogistics()

        logistics.consignee = self.c['consignee']
        logistics.area = '%s - %s' % (area.sub.name, area.name)
        logistics.address = self.c['address']
        logistics.tel = self.c['tel']
        logistics.signDate = self.c['signDate']
        logistics.signTimeStart = time.start
        logistics.signTimeEnd = time.end
        logistics.logisTimeStart = time.start.replace(hour = time.start.hour - logisticsTimeAvdce)
        logistics.logisTimeEnd = time.end.replace(hour = time.end.hour - logisticsTimeAvdce)
        logistics.note = self.c['note']

        logistics.order = self.order

        logistics.save()

        return self


    # 商品信息提交
    @subFailRemind('部分商品已下架，无法提交商品信息。')
    def itemSubmit(self):

        orderItem = []

        for v,i in self.items.items():

            item = Item.objects.getItemByItemID(id=i['itemID'])
            spec = ItemSpec.objects.getSpecBySpecID(id=i['specID']).spec
            fee = ItemFee.objects.getFeeBySpecID(specID=i['specID'])
            dis = Discount.objects.getDisByDisID(id=i['disID'])
            nowFee = forMatFee(fee.amount * Decimal(dis.discount))

            orderItem.append(
                OrderItem(
                    order=self.order,
                    name=item.name,
                    sn=item.sn,
                    spec=spec.value,
                    number=i['num'],
                    amount=fee.amount,
                    discount=dis.discount,
                    nowFee=nowFee
                    )
                )


        OrderItem.objects.bulk_create(orderItem)

        return self

    # 支付信息提交
    @subFailRemind('无法提交支付信息提交。')
    def paySubmit(self):

        pay = Pay.objects.getPayById(id=self.c['pay'])

        oPay = OrderPay()
        oPay.order = self.order
        oPay.payName = pay.name
        oPay.cod = pay.cod

        oPay.save()

        return self


    # 配送方式信息提交
    @subFailRemind('无法提交配送方式信息。')
    def shipSubmit(self):

        # ship = Pay.objects.getPayById(id=self.c['ship'])

        oShip = OrderShip()
        oShip.order = self.order
        # oShip.shipName = ship.name
        # oShip.cod = ship.cod

        oShip.shipName = u'市内免费送货上门'
        oShip.cod = u'fditc'

        oShip.save()

        return self


    # 订单状态提交
    @subFailRemind('无法提订单状态。')
    def oStartSubmit(self):
        oStart = OrderStatus()
        oStart.order = self.order

        oStart.save()

        return self


    # 订单日志提交
    @subFailRemind('无法提交订单日志。')
    def oLogSubmit(self):
        oOLT = OrderLog()
        oOLT.order = self.order
        oOLT.user = self.request.user

        oOLT.save()

        return self


    # 删除新订单
    def delNewOrder(self):
        self.order.delete()

        return self


    # 订单提交完成
    @subFailRemind('订单提交无法完成。')
    def submitDone(self):
        Cart(self.request).clear()
        ShipConsignee(self.request).clear()
        Order(self.request).clear()


        return self


    # 显示订单号,主要用于前提用户级提示
    def showOrderSN(self):
        if self.error:
            return self.showError()
        else:
            messages.success(self.request, '您已成功提交订单!')
            messages.success(self.request, '感谢您在本店购物！请记住您的订单号: %s' % self.orderId)

            return HttpResponseRedirect('/')


    # 重定向至订单列表页
    def redirOrder(self):
        if self.error:
            return self.showError()
        else:
            messages.success(self.request, '订单提交成功: %s' % self.orderId)

            return HttpResponseRedirect('/order/')


    # 粗粒用户级错误提示
    def showError(self):
        messages.error(self.request, '订单提交失败，请重新提交。')

        return redirectBack(self.request)



class OrderListPurview:
    """
    订单列表权限加持

    获取当前角色可进行的订单操作权限.
    获取订单状态,判定可选权限.
    两者进行交集操作.


    """

    def __init__(self, oList, request):
        self.oList = oList
        self.role = OrderStatus.oStatus


    # 获取订单可选操作项
    def getElement(self):

        for i in self.oList:

            if not i.orderstatus.orderStatus:

                i.action = (
                            (1, u'确认'),
                            (2, u'编辑'),
                            (3, u'无效'),
                            )

            elif i.orderstatus.orderStatus == 2: #编辑

                i.action = (
                            (1, u'确认'),
                            (2, u'编辑'),
                            (3, u'无效'),
                            )

            elif i.orderstatus.orderStatus == 3: #无效

                i.action = (
                                (6, u'新单'),
                            )

            elif i.orderstatus.orderStatus == 5: #停止

                i.action = (
                                (6, u'新单'),
                            )

            else:
                i.action = ()

        return self


    def beMixed(self):
        for i in self.oList:
            i.action = (i for i in i.action if i in self.role)

        return self.oList