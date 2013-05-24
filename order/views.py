#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from signtime.models import *
from message.views import *
from cart.views import *
from office.func import *
from area.models import *
from item.models import *
from payment.models import *
from models import *
from forms import *
from consignee.forms import *
import time, json
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
    items = Cart(request).showItemToCart()

    form = getForms(request)

    return render_to_response('orderneworedit.htm', locals(), context_instance=RequestContext(request))



def adminOrderSubmit(request):

    if request.method == 'POST':

        return OrderSubmit(request).adminSubmit()

    else:
        return Message(request).redirect().warning('订单提交方式错误 !').officeMsg()


def addItemToOrder(request):

    if request.method == 'POST':

        Cart(request).pushToCartByItemIDs(request.POST.getlist('i'))

        return HttpResponseRedirect('/order/new/')

    else:
        return Message(request).redirect().warning('订单提交方式错误 !').officeMsg()




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
        self.template = ''
        self.items = Cart(self.request).items
        self.c = ShipConsignee(self.request).c

    def submit(self):
        # 插入订单号占位！
        # 插入订单基本信息
        # 插入订单物流信息
        # 插入订单商品信息
        # 插入订单规格信息
        # 插入订单支付方式信息
        # 插入订单送货方式信息
        # 插入订单订单状态
        # 插入订单订单时间线
        # 插入订单完成

        self.newOderSn() \
            .infoSubmit() \
            .logisticsSubmit() \
            .itemSubmit() \
            .specSubmit() \
            .paySubmit() \
            .shipSubmit() \
            .oStartSubmit() \
            .oLineSubmit() \
            .submitDone()


        if self.error:
            self.delNewOrder()

        return self.message


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


    # 插入订单基本信息
    def infoSubmit(self, u= '' , r ='网店订单'):

        self.order.referer=r
        self.order.user= u if u else self.request.user.username

        self.order.save()


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
        logistics.signDate = c['signDate']
        logistics.signTimeStart = time.start
        logistics.signTimeEnd = time.end
        logistics.note = c['note']

        logistics.order = self.order

        logistics.save()

        return self


    def itemSubmit(self):

        self.orderItem = []

        for i in self.items:

            item = Item.objects.getItemBySpecId(id=i['specID'])

            self.orderItem.append(OrderItem(order=self.order, name=item.name,sn=item.sn))

            # 删除重复项
            self.orderItem = list(set(self.orderItem))

        OrderItem.objects.bulk_create(self.orderItem)

        return self


    def specSubmit(self):
        self.orderSpec = []

        for i in self.items:

            spec = ItemSpec.objects.getSpecBySpecID(id=i['specID'])

            orderItem = OrderItem.objects.get(order=self.order, sn=spec.item.sn)

            sp = OrderSpec()

            sp.orderItem = orderItem
            sp.spec = spec.spec

            sp.save()

            self.feeSubmit(sp, spec, i)

        return self


    def feeSubmit(self, sp, spec, i):

        oFee = OrderFee()
        oFee.orderSpec = sp
        oFee.number = i['num']
        oFee.amount = ItemFee.objects.getFeeBySpecID(specID=i['specID']).amount
        oFee.save()

        return self.disSubmit(oFee, spec, i)


    def disSubmit(self, oFee, spec, i):

        oDis = OrderDiscount()
        oDis.orderFee = oFee
 
        oDis.discount = ItemDiscount.objects.getDisByDisID(disID=i['disID']).discount

        oDis.save()

        return self

    def disSubmitByAdmin(self,oFee, spec):
        pass



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