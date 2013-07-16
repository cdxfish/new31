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
from purview.views import *
import time, json, datetime
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.

# 订单列表显示页面
def orderList(request):
    o = OrderSerch(request)

    form = OrderStatusForm(initial=o.initial)

    oList = o.baseSearch().chcs().range().page()
    oList = OrderListPurview(oList, request).getElement().mixedStatus()

    return render_to_response('orderlist.htm', locals(), context_instance=RequestContext(request))


# 后台订单提交,提交成功后进行页面跳转至订单列表
@checkPOST
def submit(request):

    ShipConsignee(request).setSeesion()

    return OrderSubmit(request).submit().redirOrder()


# 后台新单编辑操作编辑页面
def newOrderUI(request):
    a = request.session['o']
    o = Order(request)
    o.o['status'] = 0

    return editUI(request)

def editOrderUI(request, c=1):

    # 将订单信息配置到seesion当中
    ShipConsignee(request).setSiessionByOrder(sn=SN)
    o = Order(request)
    o.cCon(c)
    oFormat = o.oFormat.copy()
    oFormat['typ'] = OrderInfo.objects.get(sn=SN).typ
    oFormat['status'] = c
    oFormat['sn'] = SN

    o.setSeesion(oFormat)

    return editUI(request)


# 后台订单编辑操作编辑页面
def editUI(request):

    items = Cart(request).showItemToCart()

    form = getForms(request)

    oTypeForm = getOTpyeForm(request)

    return render_to_response('orderneworedit.htm', locals(), context_instance=RequestContext(request))


# 非新单及编辑以外的订单操作
def cCon(request, c):

    return Order(request).cCon(c)


# 后台订单编辑中添加商品至订单操作
@checkPOST
@decoratorBack
def addItemToOrder(request, kwargs):

    return Cart(request).pushToCartByItemIDs(request.POST.getlist('i'))


# 编辑界面中删除订单中的商品操作
@decoratorBack
def delItemToOrder(request, kwargs):

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

    def cCon(self, c):
        c = int(c)
        SN = self.request.GET.get('sn')
        order =  OrderInfo.objects.get(sn=SN).orderstatus
        act = OrderStatus.objects.getActTuple(order.status)

        if not c in act:

            messages.error(self.request, u'%s - 无法%s' % (SN, order.get_status_display()))

            return redirectBack(self.request)

        order.status = c

        order.save()

        return self

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

        self.oList = self.oList.filter(orderlog__time__range=(self.initial['s'], self.initial['e']), orderlog__log=0)

        return self

    def page(self):

        return page(l=self.oList, p=int(self.request.GET.get('p', 1)))


class OrderSubmit:
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

        self.items = Cart(self.request).items
        self.c = ShipConsignee(self.request).c
        self.o = Order(self.request).o


    def submit(self):

        if self.o['status']:
            pass
        else:

            self.newOderSn() \
                .infoSubmit() \
                .logisticsSubmit() \
                .itemSubmit() \
                .paySubmit() \
                .shipSubmit() \
                .oStartSubmit() \
                .oLogSubmit()
                # .submitDone()

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
                self.order = OrderInfo.objects.get(sn=self.orderId)

            except:
                run = False

                self.order = OrderInfo.objects.create(sn=self.orderId)

            else:
                self.orderId += 1

        return self


    # 插入订单基本信息
    @subFailRemind('会员不存在，无法提交订单基本信息。')
    def infoSubmit(self):
        if self.c['user']:
            self.order.user= User.objects.get(username=self.c['user'])

        self.order.typ = self.o['typ']
        self.order.save()

        return self


    # 物流信息提交
    @subFailRemind('无法提交物流信息。')
    def logisticsSubmit(self):

        logisticsTimeAvdce = 1

        time = SignTime.objects.get(id=self.c['time'], onl=True)

        area = Area.objects.get(id= self.c['area'], onl=True)

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
            fee = ItemFee.objects.getFeeBySpecID(id=i['specID'])
            dis = Discount.objects.getDisByDisID(id=i['disID'])
            nfee = forMatFee(fee.fee * Decimal(dis.dis))

            orderItem.append(
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

        OrderItem.objects.bulk_create(orderItem)

        return self

    # 支付信息提交
    @subFailRemind('无法提交支付信息提交。')
    def paySubmit(self):

        pay = Pay.objects.getPayById(id=self.c['pay'])

        oPay = OrderPay()
        oPay.order = self.order
        oPay.name = pay.name
        oPay.cod = pay.cod

        oPay.save()

        return self


    # 配送方式信息提交
    @subFailRemind('无法提交配送方式信息。')
    def shipSubmit(self):

        # ship = Pay.objects.getPayById(id=self.c['ship'])

        oShip = OrderShip()
        oShip.order = self.order
        # oShip.name = ship.name
        # oShip.cod = ship.cod

        oShip.name = u'市内免费送货上门'
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



class OrderListPurview(OrderPurview):
    """
        订单列表权限加持

        获取当前角色可进行的订单操作权限.
        获取订单状态,判定可选权限.
        两者进行交集操作.

    """

    def __init__(self, oList, request):
        super(OrderListPurview, self).__init__(oList, request)
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