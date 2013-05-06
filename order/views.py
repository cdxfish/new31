#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from signtime.models import *
from message.views import *
from cart.views import *
from office.func import *
from area.models import *
from item.models import *
from payment.models import *
from models import *
import time
from django.conf import settings

# Create your views here.

def orderList(request):


    c = request.GET.get('c') if request.GET.get('c') else 0
    s = request.GET.get('s')
    e = request.GET.get('e')
    k = request.GET.get('k') if request.GET.get('k') else ''
    p = int(request.GET.get('p')) if request.GET.get('p') > 0 else 1


    oListAll = OrderInfo.objects.select_related().all()

    oList = page(l=oListAll, p=p)

    return render_to_response('orderlist.htm', locals(), context_instance=RequestContext(request))

def orderSubmit(request):
    if request.method == 'POST':

        return OrderSubmit(request).submit()

    else:
        return Message(request).redirect().warning('订单提交方式错误 !').shopMsg()


def newOrEditOrderUI(request):

    pay = Pay.objects.filter(onLine=True)
    signtime = SignTime.objects.filter(onLine=True)

    area = Area.objects.filter(onLine=True,sub=None)

    toDay = time.gmtime()
    cDate = time.strptime(request.session['c']['date'], '%Y-%m-%d')

    if cDate < toDay:
        request.session['c']['date'] = '%s' % datetime.date.today()

    return render_to_response('orderneworedit.htm', locals(), context_instance=RequestContext(request))





class OrderSubmit:
    """docstring for Order"""
    def __init__(self, r):
        self.request = r
        self.orderId = 2013113082322
        self.orderItem = []
        self.orderSpec = []
        self.orderFee = []
        self.orderDiscount = []
        self.error = False
        self.message = ''

    def submit(self):
        # 插入订单号占位！
        # 插入订单基本信息
        # 插入订单物流信息
        # 插入订单商品信息
        # 插入订单支付方式信息
        # 插入订单送货方式信息
        # 插入订单送货方式信息
        # 插入订单订单状态
        # 插入订单订单时间线
        # 插入订单完成

        if settings.DEBUG:
            self.newOderSn() \
                .infoSubmit() \
                .logisticsSubmit() \
                .itemSubmit() \
                .paySubmit() \
                .shipSubmit() \
                .oStartSubmit() \
                .oLineSubmit() \
                .submitDone()
        else:
            self.newSnForMsg() \
                .infoForMsg() \
                .logisticsForMsg() \
                .itemForMsg() \
                .payForMsg() \
                .shipForMsg() \
                .oStartForMsg() \
                .oLineForMsg() \
                .submitDone()

        if self.error:
            self.delNewOrder()

        return self.message



    def newSnForMsg(self):
        # 新订单锁定
        if not self.error:
            try:
                self.newOderSn()
            except:
                self.errorMsg(Message(self.request).redirect().error('无法插入订单号！').shopMsg())

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

        runOrder = True

        while runOrder:
            try:
                self.order = OrderInfo.objects.get(orderSn=self.orderId)

            except:
                runOrder = False

                self.order = OrderInfo.objects.create(orderSn=self.orderId)
                
            else:
                self.orderId += 1

        return self


    def infoForMsg(self):
        # 插入基本信息
        if not self.error:
            try:
                self.infoSubmit()
            except :
                self.errorMsg(Message(self.request).redirect().error('无法插入订单基本信息，请重新提交订单或联系客服！').shopMsg())

        return self


    # 插入订单基本信息
    def infoSubmit(self, u= '' , r ='网店订单'):

        self.order.referer=r
        self.order.user= u if u else self.request.user.username

        self.order.save()


        return self


    def logisticsForMsg(self):
        # 插入订单物流信息
        if not self.error:
            try:
                self.logisticsSubmit()
            except :
                self.errorMsg(Message(self.request).redirect(url='/cart/consignee/').error('收货信息有误，请重新填写！').shopMsg())

        return self


    # 插入订单物流信息
    def logisticsSubmit(self):

        c = self.request.session['c']

        time = SignTime.objects.get(id=c['time'], onLine=True)

        area = Area.objects.get(id= c['area'], onLine=True)

        logistics = OrderLogistics()

        logistics.consignee = c['consignee']
        logistics.area = '%s - %s' % (area.sub.name, area.name)
        logistics.address = c['address']
        logistics.tel = c['tel']
        logistics.signDate = c['date']
        logistics.signTimeStart = time.start
        logistics.signTimeEnd = time.end
        logistics.note = c['note']

        logistics.order = self.order

        logistics.save()

        return self


    def itemForMsg(self):
        # 插入商品信息
        if not self.error:
            try:
                self.itemSubmit()

            except :
                self.errorMsg(Message(self.request).redirect(url='/cart/').error('当前购物车中商品已下降，请重新选择商品或联系客服！').shopMsg())

        return self


    def itemSubmit(self):

        self.orderItem = []

        for v, i in self.request.session['itemCart'].items():

            item = Item.objects.getItemByItemSpecId(id='%s' % v[1:])

            self.orderItem.append(OrderItem(order=self.order, name=item.name,sn=item.sn))

            # 删除重复项
            self.orderItem = list(set(self.orderItem))

        OrderItem.objects.bulk_create(self.orderItem)

        return self.specForMsg()


    def specForMsg(self):
        # 插入商品规格信息
        if not self.error:
            try:
                return self.specSubmit()

            except :
                self.errorMsg(Message(self.request).redirect(url='/cart/').error('当前购物车中商品规格有误，请重新选择商品或联系客服！').shopMsg())

        return self

    def specSubmit(self):
        self.orderSpec = []

        for v, i in self.request.session['itemCart'].items():

            spec = ItemSpec.objects.getSpecByItemSpecId(id='%s' % v[1:])

            orderItem = OrderItem.objects.get(order=self.order, sn=spec.item.sn)

            sp = OrderSpec()

            sp.orderItem = orderItem
            sp.spec = spec.spec

            sp.save()

            self.feeForMsg(sp, spec, v, i)

        return self


    def feeForMsg(self, sp, spec, v, i):
        # 插入商品价格信息
        if not self.error:
            try:
                return self.feeSubmit(sp, spec, v, i)

            except :
                self.errorMsg(Message(self.request).redirect(url='/cart/').error('当前购物车中商品价格有误，请重新选择商品或联系客服！').shopMsg())

        return self

    def feeSubmit(self, sp, spec, v, i):

        oFee = OrderFee()
        oFee.orderSpec = sp
        oFee.number = i
        oFee.itemType = v[0]
        oFee.amount = spec.itemfee_set.get(itemType=v[0]).amount
        oFee.save()

        return self.disForMsg(oFee, spec, v)


    def disForMsg(self, oFee, spec, v):
        # 插入商品折扣信息
        if not self.error:
            try:
                return self.disSubmit(oFee, spec, v)

            except :
                self.errorMsg(Message(self.request).redirect(url='/cart/').error('当前购物车中商品折扣有误，请重新选择商品或联系客服！').shopMsg())

        return self

    def disSubmit(self, oFee, spec, v):
        if v[0] == '1': 

            oDis = OrderDiscount()
            oDis.orderFee = oFee
            
            if self.request.user.is_authenticated():
                oDis.discount = spec.itemfee_set.get(itemType=int(v[0])).itemdiscount_set.all()[0].discount.discount
            else:
                oDis.discount = 10.0

            oDis.save()

        return self


    def payForMsg(self):
        # 插入商品支付方式信息
        if not self.error:
            try:
                return self.paySubmit()

            except :
                self.errorMsg(Message(self.request).redirect(url='/cart/consignee/').error('当前支付方式信息有误，请重新选择或联系客服！').shopMsg())

        return self

    def paySubmit(self):

        pay = Pay.objects.getPayById(id=self.request.session['c']['pay'])

        oPay = OrderPay()
        oPay.order = self.order
        oPay.payName = pay.name
        oPay.cod = pay.cod

        oPay.save()

        return self


    def shipForMsg(self):
        # 插入商品送货方式信息
        if not self.error:
            try:
                return self.shipSubmit()

            except :
                self.errorMsg(Message(self.request).redirect(url='/cart/consignee/').error('当前送货方式信息有误，请重新选择或联系客服！').shopMsg())

        return self


    def shipSubmit(self):

        # ship = Pay.objects.getPayById(id=self.request.session['c']['ship'])

        oShip = OrderShip()
        oShip.order = self.order
        # oShip.shipName = ship.name
        # oShip.cod = ship.cod

        oShip.shipName = u'市内免费送货上门'
        oShip.cod = u'fditc'

        oShip.save()

        return self

    def oStartForMsg(self):
        # 插入订单状态信息
        if not self.error:
            try:
                return self.oStartSubmit()

            except :
                self.errorMsg(Message(self.request).redirect(url='/cart/').error('无法正确配置当前订单状态，请重新下单或联系客服！').shopMsg())

        return self

    def oStartSubmit(self):
        oStart = OrderStatus()
        oStart.order = self.order

        oStart.save()

        return self

    def oLineForMsg(self):
        # 插入订单状态信息
        if not self.error:
            try:
                return self.oLineSubmit()

            except :
                self.errorMsg(Message(self.request).redirect(url='/cart/').error('无法正确配置当前订单时间线，请重新下单或联系客服！').shopMsg())

        return self

    def oLineSubmit(self):
        oOLT = OrderLineTime()
        oOLT.order = self.order

        oOLT.save()

        return self


    def errorMsg(self, m=''):
        self.error = True
        self.message =  m

        return self


    def delNewOrder(self):
        self.order.delete()

        return self


    def submitDone(self):
        if not self.error:
            self.message = Message(self.request).success('您已成功提交订单!').info('感谢您在本店购物！请记住您的订单号: %s' % self.orderId).shopMsg()
            # Cart(self.request).clearCart()
            # ShipConsignee(self.request).clearConsignee()

        return self




# 订单列表权限加持
class OrderListPurview:
    """docstring for orderList"""
    def __init__(self, oList, request):
        self.oList = oList
        self.element = Element.objects.get(path=request.path).sub_set.all()


    def operation(self, order):

        pass

    # 获取订单可选操作项
    def getElement(self):

        pass