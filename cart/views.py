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
from consignee.views import *
import time, datetime
from decimal import *


# Create your views here.

def cart(request):
    a = Cart(request).items

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


def rectToCart(func):

    def newFunc(request, args):
        
        func(request, args)

        return HttpResponseRedirect('/cart/')

    return newFunc


@rectToCart
def buy(request, args):
   
    return Cart(request).pushToCart(args['specID'])


@rectToCart
def clear(request, args):

    return Cart(request).clearItemBySpec(args['specID'])


@rectToCart
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

        self.itemsFormat = []

        self.item = {
                        'itemID': 1, 
                        'specID': 1, 
                        'disID': 1, 
                        'num': 1
                    }

        self.request = request

        self.items = request.session.get('items')

    def setItems(self, items):

        self.request.session['items'] = items
        self.items = items

        return self

    def formatItems(self):
        if not self.items:

            return self.setItems(self.itemsFormat)


    def pushToCart(self, specID):
        
        item = Item.objects.getItemBySpecId(id=specID)
        items = self.items

        i = self.item

        i['itemID'] = item.id
        i['specID'] = int(specID)

        if self.request.user.is_authenticated():
            print 'a'
            i['disID'] = ItemDiscount.objects.getDisBySpecID(specID=specID).id
        else:
            print 'b'
            i['disID'] = Discount.objects.getDefault().id


        if not i in items:

            items.append(i)

            return self.setItems(items)

        else:

            return self


    def clearItemBySpec(self, specID):

        specID = int(specID)

        items = self.items

        for i in items:

            if specID == i['specID']:

                items.remove(i)

        return self.setItems(items)


    def changeNumBySpec(self, specID, num):
        specID = int(specID)
        num = int(num)

        items = self.items

        for i in items:

            if specID == i['specID']:
                i['num'] = num

        self.request.session['items'] = items

        return self


    def showItemToCart(self):

        items = self.items

        itemList = []
        countFee = 0

        for i in items:
                
            itemSpec = ItemSpec.objects.getSpecBySpecID(id=i['specID'])
            dis = Discount.objects.get(id=i['disID'])
            amount = itemSpec.itemfee_set.getFeeByNomal().amount * Decimal(dis.discount)
            total = amount * i['num']
            countFee += total

            itemList.append({ 'item': itemSpec, 'amount': amount, 'num': i['num'], 'dis': dis, 'total': total })

        return {'items': itemList, 'total': countFee}

    def clearCart(self):
        self.setItems(self.itemsFormat)

        return self

    def countFee(self):
        items = self.items

        countFee = 0

        for i in items:

            amount = ItemFee.objects.getFeeBySpecID(specID=i['specID']).amount
            total = amount * i['num']
            countFee += total

        return countFee