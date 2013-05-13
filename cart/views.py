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

# Create your views here.

def cart(request):

    cart = CartShow(request)

    return render_to_response('cart.htm', locals(), context_instance=RequestContext(request))


def checkout(request):

    if request.method == 'POST':

        form = ConsigneeForm(request.POST)

        if not form.is_valid():

            for i in form:
                if i.errors:

                    messages.warning(request, '%s - %s' % ( i.label, i.errors))

            return HttpResponseRedirect('/consignee/')

        cart = CartShow(request)

        if not cart:

            return Message(request).redirect(url='/cart/').error('您还没选择商品喔亲~').shopMsg()

        ShipConsignee(request).setSeesion()

        pay = Pay.objects.getPayById(id=request.POST.get('pay'))
        time = SignTime.objects.getTimeById(id=request.POST.get('time'))
        area = Area.objects.getAreaById(id=request.POST.get('area'))

        return render_to_response('checkout.htm', locals(), context_instance=RequestContext(request))
    else:

        return Message(request).redirect(url='/consignee/').error('提交方式有误').shopMsg()

def buy(request, specID):


    return Cart(request).pushToCart(specID)


class CartShow:
    """购物车"""
    def __init__(self, request):
        self.itemBuy = []
        self.countFee = 0
        self.request = request
        self.items = []
        itemCart = self.request.session.get('items')
        if itemCart:
            for v, i in itemCart.items():
                try:
                    if len(v) < 2:
                        raise Item.DoesNotExist
                        
                    itemSpec = ItemSpec.objects.getSpecByItemSpecId(id='%s' % v[1:])
                    amount = itemSpec.itemfee_set.get(itemType=v[0]).amount
                    subtotal = amount * i
                    self.countFee += subtotal
                    self.itemBuy.append({ 'item': itemSpec, 'amount': amount, 'num': i,'subtotal': subtotal, 'v': v })
                except:
                    del itemCart[v]

            self.request.session['c'] = itemCart


    def cartItemSubtotal(self, i, t):
        itemCart = self.request.session["items"]
        itemSubtotal = ItemSpec.objects.getSpecByItemSpecId(id='%s' % i[1:]).itemfee_set.get(itemType=i[0]).amount * int(t)

        return itemSubtotal

    def clearCart(self):
        self.request.session['items'] = {}

        return self


class Cart:
    """ 购物车相关

        items 

        用于存储购物车中商品信息
        其数据格式为:
        [{ itemID:1, specID:1, num:1 }, { itemID:2, specID:2, num:2 }]

    """
    def __init__(self, request):

        self.items = []

        self.request = request

    def showToCart(self):
        pass



    def hCart(request, func, id):

        if settings.DEBUG:

            return func(request, id)

        else:
            try:

                return func(request, id)
            except:
                return Message(request).redirect(url=request.META.get('HTTP_REFERER',"/")).warning('当前商品已下架').shopMsg()



    def pushToCart(self, specID):
        
        item = Item.objects.getItemBySpecId(id=specID)

        # itemCart = request.session['item']

        # if not i in request.session['item']:
        #     itemCart.update({ '%s%s' % (t,i):1 })

        # request.session['item'] = itemCart

        return HttpResponseRedirect('/cart/')


    def clearCartItem(request, i , t= 1):
        try:
            if not request.session.get('itemCart'):
                request.session["itemCart"] = {}

            itemCart = request.session["itemCart"]

            a = '%s%s' % (t,i)

            if a in itemCart:
                del itemCart[a]

            request.session['itemCart'] = itemCart

            return request
        except:
            raise Item.DoesNotExist

    def changeCartItem(request, i , t):
        try:
            item = Item.objects.getItemByItemAttrId(id='%s' % i[1:])

            itemCart = request.session["itemCart"]

            if i in itemCart:
                itemCart[i] = int(t)

            request.session['itemCart'] = itemCart

            return request
        except:
            raise Item.DoesNotExist