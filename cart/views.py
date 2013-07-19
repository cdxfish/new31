#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import *
from signtime.models import *
from account.models import *
from payment.models import *
from item.models import *
from area.models import *
from consignee.views import *
from new31.func import *
from new31.decorator import *
import time, datetime, math
from decimal import *


# Create your views here.

# 前台购物车界面
def cart(request):
    cart = Cart(request).showItemToCart()

    return render_to_response('cart.htm', locals(), context_instance=RequestContext(request))

# 前台订单确认界面
@checkPOST
def checkout(request):

    form = ConsigneeForm(request.POST)

    if not form.is_valid():

        for i in form:
            if i.errors:

                messages.warning(request, '%s - %s' % ( i.label, i.errors))

        return HttpResponseRedirect('/consignee/')

    cart = Cart(request).showItemToCart()

    if not cart:

        messages.warning(request, '购物车内无商品')

        return HttpResponseRedirect('/cart/')

    request.session['c']['user'] = request.user.username

    SpCnsgn(request).setSeesion()

    pay = Pay.objects.getPayById(id=request.POST.get('pay'))
    time = SignTime.objects.getTimeById(id=request.POST.get('time'))
    area = Area.objects.getAreaById(id=request.POST.get('area'))

    return render_to_response('checkout.htm', locals(), context_instance=RequestContext(request))

# 前台订单提交,并是用前台消息模板显示订单号等信息
@checkPOST
def submit(request):
    from order.views import OrdSub

    return OrdSub(request).submit().showOrdSN()

# GET方式将物品放入购物车
@rdrBckDr
@itemonl
def buy(request, kwargs):
   
    return Cart(request).pushToCartBySpecID(kwargs['specID'])

# GET方式将物品取出购物车
@rdrBckDr
@itemonl
def clear(request, kwargs):

    return Cart(request).clearItemByMark(kwargs['mark'])


class Cart(object):
    """ 
        购物车相关

        request.session['items'] 

        用于存储购物车中商品信息
        其数据格式为:
        [
            { 'mark':1, 'itemID':1, 'specID':1, 'num':1 }, 
            { 'mark':2, 'itemID':2, 'specID':2, 'num':2 },
            .........
        ]

        此类包含有对购物车操作的各类方法(必须实例化方可使用)

        example:
            Cart(request).clearItemByMark(mark)


    """
    def __init__(self, request):

        self.itemsFormat = {}

        self.item = {
                        'mark':0,
                        'itemID': 0, 
                        'specID': 0, 
                        'disID': 0, 
                        'num': 1
                    }

        self.request = request

        self.items = request.session.get('items')

    def setSeesion(self, items):

        self.request.session['items'] = items

        return self

    def formatItems(self):
        if not self.items:

            return self.setSeesion(self.itemsFormat)

    def formatMark(self):

        t = time.gmtime()
        tCount = t.tm_hour * t.tm_min * t.tm_sec
        sExpiryDate = self.request.session.get_expiry_date()
        sCount = (sExpiryDate.hour * sExpiryDate.minute * sExpiryDate.second ) % 10

        return int('%d%05d%d' % (len(self.items) + 1, tCount, sCount ))


    def pushToCartBySpecID(self, specID):
        specID = int(specID)

        items = self.items

        i = self.item.copy()

        i['itemID'] = Item.objects.getItemBySpecId(id=specID).id
        i['specID'] = ItemSpec.objects.getSpecBySpecID(specID).id
        i['mark'] = self.formatMark()

        if self.request.user.is_authenticated():

            i['disID'] = ItemFee.objects.getDisBySpecID(id=specID).id
        else:
            
            i['disID'] = Discount.objects.getDefault().id

        items.update({i['mark']: i}) 

        return self.setSeesion(items)


    def pushToCartByItemIDs(self, itemIDs):
        items = self.items

        for i in itemIDs:
            ii = self.item.copy()

            item = Item.objects.getItemByItemID(i)

            ii['mark'] = self.formatMark()
            ii['itemID'] = item.id
            ii['specID'] = item.itemspec_set.getDefaultSpec().id
            ii['disID'] = Discount.objects.getDefault().id
  
            items[ii['mark']] = ii 

        return self.setSeesion(items)

    def pushItem(self, items):
        _items = self.items

        for i in items:

            i['mark'] = self.formatMark()
  
            _items[i['mark']] = i  

        return self.setSeesion(_items)


    def clearItemByMark(self, mark):

        mark = int(mark)

        items = self.items

        del items[mark]

        return self.setSeesion(items)


    def changeNumBySpec(self, mark, num):
        mark = int(mark)
        num = int(num)

        items = self.items

        items[mark]['num'] = num

        self.request.session['items'] = items

        return self


    def showItemToCart(self):

        items = self.items
        _items = self.items.copy()

        itemList = []
        countFee = 0

        for i in items:
            try:
                ii = self.getItemTotalByMark(i)
                countFee += ii['total']

                itemList.append(ii)
            except Exception, e:
                del _items[i]
                messages.warning(self.request, '部分商品已下架。')

        self.setSeesion(_items)

        return {'items': itemList, 'total': forMatFee(countFee)}

    def clear(self):
        self.items.clear()
 
        return self.setSeesion(self.items)

    def countFee(self):
        cart = self.showItemToCart()

        return cart['total']

    def changeItem(self):

        name =  self.request.GET.get('name')
        mark =  self.request.GET.get('mark')
        value =  self.request.GET.get('value', 0)

        items = self.items

        items[int(mark[1:])][name] = int(value)

        return self.setSeesion(items)

    def getItemTotalByMark(self, mark):
        i = self.items[mark]

        item = Item.objects.getItemByItemID(id=i['itemID'])
        spec = item.itemspec_set.getSpecBySpecID(id=i['specID'])
        dis = Discount.objects.get(id=i['disID'])
        fee = spec.itemfee_set.getFeeByNomal().fee * Decimal(dis.dis)
        total = fee * int(i['num'])

        return {
                'mark': i['mark'],
                'item': item,
                'spec': spec, 
                'fee': forMatFee(fee), 
                'num': i['num'], 
                'dis': dis, 
                'total': forMatFee(total)
            }
