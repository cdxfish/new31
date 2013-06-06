#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import *
from django.db.models import Q
from signtime.models import *
from account.models import *
from payment.models import *
from message.views import *
from item.models import *
from area.models import *
from order.models import *
from order.forms import *
from consignee.views import *
from new31.func import *
import time, datetime, math
from decimal import *


# Create your views here.

def cart(request):
    a = request.session.get('items')
    c = request.session['c']
    if settings.DEBUG:

        cart = Cart(request).showItemToCart()
    else:
        try:

            cart = Cart(request).showItemToCart()
        except:

            Cart(request).clearCart()
            return Message(request).redirect(url='/cart/').error('您购物车中有些商品已过期，请重新选择。').shopMsg()


    return render_to_response('cart.htm', locals(), context_instance=RequestContext(request))


def checkout(request):

    if request.method == 'POST':

        form = ConsigneeForm(request.POST)

        if not form.is_valid():

            for i in form:
                if i.errors:

                    messages.warning(request, '%s - %s' % ( i.label, i.errors))

            return HttpResponseRedirect('/consignee/')

        cart = Cart(request).showItemToCart()

        if not cart:

            return Message(request).redirect(url='/cart/').error('您还没选择商品喔亲~').shopMsg()

        ShipConsignee(request).setSeesion()

        pay = Pay.objects.getPayById(id=request.POST.get('pay'))
        time = SignTime.objects.getTimeById(id=request.POST.get('time'))
        area = Area.objects.getAreaById(id=request.POST.get('area'))

        return render_to_response('checkout.htm', locals(), context_instance=RequestContext(request))
    else:

        return Message(request).redirect(url='/consignee/').error('提交方式有误').shopMsg()


def hFunc(request, func, **args):

    if settings.DEBUG:

        return func(request, args)

    else:
        try:

            return func(request, args)
            
        except:

            return Message(request).redirect(url=request.META.get('HTTP_REFERER',"/")).warning('当前商品已下架').shopMsg()


# 页面跳转回上一页用装饰器
def rectToBack(func):

    def newFunc(request, args):
        
        func(request, args)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER',"/"))

    return newFunc


@rectToBack
def buy(request, args):
   
    return Cart(request).pushToCartBySpecID(int(args['specID']))


@rectToBack
def clear(request, args):

    return Cart(request).clearItemByMark(args['mark'])


@rectToBack
def changnum(request, args):

    return Cart(request).changeNumBySpec(specID=args['specID'],num=args['num'])








class Cart:
    """ 购物车相关

        items 

        用于存储购物车中商品信息
        其数据格式为:
        [{ itemID:1, specID:1, num:1 }, { itemID:2, specID:2, num:2 }]

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

    def setItems(self, items):

        self.request.session['items'] = items

        return self

    def formatItems(self):
        if not self.items:

            return self.setItems(self.itemsFormat)

    def formatMark(self):

        t = time.gmtime()
        tCount = t.tm_hour * t.tm_min * t.tm_sec
        sExpiryDate = self.request.session.get_expiry_date()
        sCount = (sExpiryDate.hour * sExpiryDate.minute * sExpiryDate.second ) % 10

        return int('%d%05d%d' % (len(self.items) + 1, tCount, sCount ))


    def pushToCartBySpecID(self, specID):

        items = self.items

        i = self.item.copy()

        i['itemID'] = Item.objects.getItemBySpecId(id=specID).id
        i['specID'] = ItemSpec.objects.getSpecBySpecID(specID).id
        i['mark'] = self.formatMark()

        if self.request.user.is_authenticated():

            i['disID'] = ItemDiscount.objects.getDisBySpecID(specID=specID).id
        else:
            
            i['disID'] = Discount.objects.getDefault().id

        items.update({i['mark']: i}) 

        return self.setItems(items)


    def pushToCartByItemIDs(self, itemIDs):
        items = self.items

        for i in itemIDs:
            ii = self.item.copy()

            item = Item.objects.getItemByItemID(i)

            ii['mark'] = self.formatMark()
            ii['itemID'] = item.id
            ii['specID'] = item.itemspec_set.getDefaultSpec().id
            ii['disID'] = Discount.objects.getDefault().id
  
            items.update({ii['mark']: ii}) 

        return self.setItems(items)


    def clearItemByMark(self, mark):

        mark = int(mark)

        items = self.items

        del items[mark]

        return self.setItems(items)


    def changeNumBySpec(self, mark, num):
        mark = int(mark)
        num = int(num)

        items = self.items

        items[mark]['num'] = num

        self.request.session['items'] = items

        return self


    def showItemToCart(self):

        items = self.items

        itemList = []
        countFee = 0

        for i in items:

            ii = self.getItemTotalByMark(i)
            countFee += ii['total']

            ii.update({'forms': getItemForms(item=ii)})



            itemList.append(ii)

        return {'items': itemList, 'total': forMatFee(countFee)}

    def clearCart(self):
        self.setItems(self.itemsFormat)

        return self

    def countFee(self):
        cart = self.showItemToCart()

        return cart['total']

    def changeItem(self):

        name =  self.request.GET.get('name')
        mark =  self.request.GET.get('mark')
        value =  self.request.GET.get('value')

        items = self.items

        items[int(mark[1:])][name] = int(value)

        return self.setItems(items)

    def getItemTotalByMark(self, mark):
        i = self.items[mark]

        item = Item.objects.getItemByItemID(id=i['itemID'])
        spec = item.itemspec_set.getSpecBySpecID(id=i['specID'])
        dis = Discount.objects.get(id=i['disID'])
        amount = spec.itemfee_set.getFeeByNomal().amount * Decimal(dis.discount)
        total = amount * int(i['num'])

        return {
                'mark': i['mark'],
                'item': item,
                'spec': spec, 
                'amount': forMatFee(amount), 
                'num': i['num'], 
                'dis': dis, 
                'total': forMatFee(total)
            }