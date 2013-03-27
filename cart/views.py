#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.exceptions import *
from item.models import *
from message.views import *

# Create your views here.

def cart(request):
    cart = Cart(request)

    d = dir(ItemAttr.objects.getAttrByItemAttrId(1))
    s = request.session.get('itemCart')
    return render_to_response('cart.htm', locals(), context_instance=RequestContext(request))

def hCart(request, f, i, t = 1):
    try:
        f(request, i, t)

        return HttpResponseRedirect("/cart/")
    except:
        return Message(request.META.get('HTTP_REFERER',"/")).autoRedirect(1).title('错误').message('当前商品已下架!').printMsg()


def consignee(request):

    return render_to_response('consignee.htm', locals(), context_instance=RequestContext(request))


def toCart(request, i , t= 1):
    try:
        if not request.session['itemCart']:
            request.session["itemCart"] = {}
        item = Item.objects.getItemByItemAttrId(id=i)

        itemCart = request.session["itemCart"]


        if not i in itemCart:
            itemCart.update({ '%s%s' % (t,i):1 })

        request.session['itemCart'] = itemCart

        return request
    except:
        raise  Item.DoesNotExist


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


class Cart:
    """docstring for Cart"""
    def __init__(self, request):
        self.itemBuy = []
        self.countFee = 0
        if request.session.get('itemCart'):
            for v, i in request.session['itemCart'].items():
                # try:
                itemAttr = ItemAttr.objects.getAttrByItemAttrId(id='%s' % v[1:])
                amount = itemAttr.itemfee_set.get(itemType=v[0]).amount
                subtotal = amount * i
                self.countFee += subtotal
                self.itemBuy.append({ 'item': itemAttr, 'amount': amount, 'num': i,'subtotal': subtotal, 'v': v })
                # except:
                #     pass