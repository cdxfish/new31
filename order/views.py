#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from new31.decorator import *
from signtime.models import *
from cart.views import *
from office.func import *
from area.models import *
from item.models import *
from payment.models import *
from models import *
from forms import *
from consignee.forms import *
import time, json
from django.contrib import messages

# Create your views here.

# 订单列表显示页面
def orderList(request):

    c = request.GET.get('c') if request.GET.get('c') else 0
    s = request.GET.get('s')
    e = request.GET.get('e')
    k = request.GET.get('k') if request.GET.get('k') else ''
    p = int(request.GET.get('p')) if request.GET.get('p') > 0 else 1

    oStatus = OrderStatus.oStatus

    oListAll = OrderInfo.objects.select_related().all()

    oList = page(l=oListAll, p=p)

    oList = OrderListPurview(oList, request).getElement().beMixed()

    return render_to_response('orderlist.htm', locals(), context_instance=RequestContext(request))


# 订单信息编辑提交
def cCon(request, c):

    c = int(c)
    orderSN = request.GET.get('sn')

    # if c == 1:
    order =  OrderInfo.objects.get(orderSn=orderSN).orderstatus

    order.orderStatus = c

    order.save()


    return HttpResponseRedirect('/order/')


# 前台订单提交,并是用前台消息模板显示订单号等信息
@checkPOST
def carSub(request):

    return OrderSubmit(request).submit().showOrderSN()


# 后台订单提交,提交成功后进行页面跳转至订单列表
@checkPOST
def adminSub(request):

    # OrderSubmit(request).submit()

    return HttpResponseRedirect('/order/new/')


# 后台新单及订单编辑操作编辑页面
def newOrEditOrderUI(request):
    items = Cart(request).showItemToCart()

    form = getForms(request)

    oTypeForm = getOTpyeForm(request)

    return render_to_response('orderneworedit.htm', locals(), context_instance=RequestContext(request))


# 后台订单编辑中添加商品至订单操作
@checkPOST
# @rectToBack
def addItemToOrder(request):

    return Cart(request).pushToCartByItemIDs(request.POST.getlist('i'))


# 编辑界面中删除订单中的商品操作
# @rectToBack
def delItemToOrder(request, args):

    return Cart(request).clearItemByMark(args['mark'])





class OrderSubmit:
    """ 订单提交类.

        订单提交只需实例后, 使用 <<submit>> 方法即可
        示例: OrderSubmit(request).submit()

        订单数据来源为 session 中数据

        session['c'] = 联系人信息
        session['items'] = 商品信息
        session['oType'] = 订单类型

        

        此类已根据 setting.DEBUG 对类方法进行了 <<用户级提示>> 装饰
        当 settings.DEBUG = True 时, 用户级提示关闭, 反之开启.

    """
    def __init__(self, request):
        self.request = request
        self.orderId = 2013113082322
        self.oType = 0
        self.orderItem = []
        self.orderSpec = []
        self.orderFee = []
        self.orderDiscount = []
        self.error = False
        self.message = ''
        self.template = ''
        self.items = Cart(self.request).items
        self.c = ShipConsignee(self.request).c

    def submit(self):
        # 插入订单号占位！
        # 插入订单基本信息
        # 插入订单物流信息
        # 插入订单商品信息
        # 插入订单支付方式信息
        # 插入订单送货方式信息
        # 插入订单订单状态
        # 插入订单订单时间线
        # 插入订单完成

        self.newOderSn() \
            .infoSubmit() \
            .logisticsSubmit() \
            .itemSubmit() \
            .paySubmit() \
            .shipSubmit() \
            .oStartSubmit() \
            .oLineSubmit() \
            .submitDone()


        if self.error:
            self.delNewOrder()

        return self


    # 获得新的订单编号
    def getNewOrderSn(self):
        t = time.gmtime()
        tCount = t.tm_hour * t.tm_min * t.tm_sec
        sExpiryDate = self.request.session.get_expiry_date()
        sCount = (sExpiryDate.hour * sExpiryDate.minute * sExpiryDate.second ) % 10

        return int('%d%d%05d%d' % (t.tm_year, t.tm_yday, tCount, sCount))


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
    def infoSubmit(self, u= '' , r ='网店订单'):

        self.order.referer=r
        self.order.user= u if u else self.request.user.username

        self.order.save()


        return self

    def formatOrderType(self):
        if not 'oType' in self.request.session:

            return self.setSeesion()


    def setSeesion(self):

        self.request.session['oType'] = self.oType

        return self


    # 插入订单物流信息
    def logisticsSubmit(self):

        logisticsTimeAvdce = 1

        c = self.request.session['c']

        time = SignTime.objects.get(id=c['time'], onLine=True)

        area = Area.objects.get(id= c['area'], onLine=True)

        logistics = OrderLogistics()

        logistics.consignee = c['consignee']
        logistics.area = '%s - %s' % (area.sub.name, area.name)
        logistics.address = c['address']
        logistics.tel = c['tel']
        logistics.signDate = c['signDate']
        logistics.signTimeStart = time.start
        logistics.signTimeEnd = time.end
        logistics.logisTimeStart = time.start.replace(hour = time.start.hour - logisticsTimeAvdce)  
        logistics.logisTimeEnd = time.end.replace(hour = time.end.hour - logisticsTimeAvdce)
        logistics.note = c['note']

        logistics.order = self.order

        logistics.save()

        return self


    # 插入订单商品信息
    def itemSubmit(self):

        self.orderItem = []

        for v,i in self.items.items():

            item = Item.objects.getItemByItemID(id=i['itemID'])
            spec = ItemSpec.objects.getSpecBySpecID(id=i['specID']).spec
            fee = ItemFee.objects.getFeeBySpecID(specID=i['specID'])
            dis = Discount.objects.getDisByDisID(id=i['disID'])

            self.orderItem.append(OrderItem(order=self.order, name=item.name, sn=item.sn, spec=spec.value, number=i['num'],amount=fee.amount, discount=dis.discount))


        OrderItem.objects.bulk_create(self.orderItem)

        return self


    def paySubmit(self):

        pay = Pay.objects.getPayById(id=self.c['pay'])

        oPay = OrderPay()
        oPay.order = self.order
        oPay.payName = pay.name
        oPay.cod = pay.cod

        oPay.save()

        return self


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


    def oStartSubmit(self):
        oStart = OrderStatus()
        oStart.order = self.order

        oStart.save()

        return self


    def oLineSubmit(self):
        oOLT = OrderLineTime()
        oOLT.order = self.order

        oOLT.save()

        return self


    def delNewOrder(self):
        self.order.delete()

        return self


    def submitDone(self):
        if not self.error:
            Cart(self.request).clearCart()
            ShipConsignee(self.request).clearConsignee()

        return self

    def showOrderSN(self):

        return Message(self.request).success('您已成功提交订单!').info('感谢您在本店购物！请记住您的订单号: %s' % self.orderId).shopMsg()

    def redirect(self, url):

        return HttpResponseRedirect(url)


# 订单列表权限加持
class OrderListPurview:
    """首先获取当前角色可进行的订单操作权限. 其后获取订单的可选操作. 两者进行交集"""
    def __init__(self, oList, request):
        self.oList = oList
        self.oStart = OrderStatus.oStatus
        self.element = Element.objects.get(path=request.path).sub_set.all()
        self.role = OrderStatus.oStatus
        (
                (0, u'新单'), 
                (1, u'确认'), 
                (2, u'编辑'),
                (3, u'无效'),
                (4, u'完成'),
                (5, u'停止'),
                (6, u'重建'),
                (7, u'更换'),
            )


    # 获取订单可选操作项
    def getElement(self):


        for i in self.oList:
            if not i.orderstatus.orderStatus:

                i.action = (
                            (1, u'确认'), 
                            (2, u'编辑'),
                            (3, u'无效'),
                            )
            # elif i.orderstatus.orderStatus == 1: #确认

            #     i.action = (
            #                     (5, u'停止'),
            #                 )
            elif i.orderstatus.orderStatus == 2: #编辑

                i.action = (
                            (1, u'确认'), 
                            (2, u'编辑'),
                            (3, u'无效'),
                            )

            elif i.orderstatus.orderStatus == 3: #无效

                i.action = (
                                (6, u'重建'),
                            )

            elif i.orderstatus.orderStatus == 5: #停止

                i.action = (
                                (6, u'重建'),
                                (7, u'更换'),
                            )

            else:
                i.action = ()

        return self


    def beMixed(self):
        for i in self.oList:
            i.action = (i for i in i.action if i in self.role)

        return self.oList