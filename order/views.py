#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from signtime.models import *
from message.views import *
from area.models import *
from item.models import *
from models import *
import time

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
        self.error = False
        self.message = ''

    def submit(self):
        self.submitNewSn().submitInfo().submitLogistics().submitItem().submitDone()

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

    def submitNewSn(self):
        # 新订单锁定
        try:
            self.newOderSn()
        except:
            self.errorMsg(Message(self.request).redirect().error('无法插入订单号！').shopMsg())

        return self



    # 插入订单基本信息
    def submitOrderInfo(self, u= '' , r ='网店订单'):

        self.order.referer=r
        self.order.user= u if u else self.request.user.username

        self.order.save()


        return self


    def submitInfo(self):
        # 插入基本信息
        try:
            self.submitOrderInfo()
        except :
            self.errorMsg(Message(self.request).redirect().error('无法插入订单基本信息！').shopMsg())

        return self



    # 插入订单物流信息
    def submitOrderLogistics(self):

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


    def submitLogistics(self):
        # 插入物流信息
        try:
            self.submitOrderLogistics()
        except :
            self.errorMsg(Message(self.request).redirect(url='/cart/consignee/').error('收货信息有误，请重新填写！').shopMsg())

        return self

    def submitOrderItem(self):
        itemList = []

        for v, i in self.request.session['itemCart'].items():

            item = Item.objects.getItemByItemSpecId(id='%s' % v[1:])

            itemList.append(OrderItem(order=self.order, item=item.itemName,sn=item.sn))

            # 删除重复项
            itemList = list(set(itemList))

        OrderItem.objects.bulk_create(itemList)

        return self

    def submitItem(self):
        # 插入商品信息
        try:
            self.submitOrderItem()

        except :
            self.errorMsg(Message(self.request).redirect(url='/cart/').error('当前购物车中已下架，请重新选择商品！').shopMsg())

        return self


    def submitDone(self):
        self.message = Message(self.request).success('您已成功提交订单!').info('感谢您在本店购物！请记住您的订单号: %s' % self.orderId).shopMsg()

        return self


    def errorMsg(self, m=''):
        self.error = True
        self.message =  m

        return self

    def delNewOrder(self):
        pass