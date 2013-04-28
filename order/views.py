#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from signtime.models import *
from message.views import *
from cart.views import *
from area.models import *
from item.models import *
from models import *
import time
from django.conf import settings

# Create your views here.

def orderList(request):

    c = request.GET.get('c') if request.GET.get('c') else 0
    s = request.GET.get('s')
    e = request.GET.get('e')
    k = request.GET.get('k') if request.GET.get('k') else ''
    p = request.GET.get('p') if request.GET.get('p') else 1

    return render_to_response('orderlist.htm', locals(), context_instance=RequestContext(request))

def orderSubmit(request):
    if request.method == 'POST':

        return OrderSubmit(request).submit()

    else:
        return Message(request).redirect().warning('订单提交方式错误 !').shopMsg()





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
        # 插入订单商品规格信息
        # 插入订单商品价格信息
        # 插入订单完成

        if settings.DEBUG:
            self.newOderSn().infoSubmit().logisticsSubmit().itemSubmit().submitDone()
        else:
            self.newSnForMsg().infoForMsg().logisticsForMsg().itemForMsg().submitDone()

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
            dis = spec.itemfee_set.get(itemType=int(v[0])).itemdiscount_set.all()[0].discount.discount
            oDis = OrderDiscount()
            oDis.orderFee = oFee
            oDis.discount = dis
            oDis.save()

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