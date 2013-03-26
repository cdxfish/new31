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

    d = dir(Item.objects.getTagByItemFeeId(id='2').itemattr_set)
    return render_to_response('cart.htm', locals(), context_instance=RequestContext(request))

def buy(request, i):
    if not request.session.get('buy'):
        request.session["buy"] = {}

    data = {}
    try:
        buy = request.session["buy"]
        item = ItemFee.objects.get(id=i).itemAttr.itemName

        if not item.onLine or not item.show:
            raise ObjectDoesNotExist

        if not i in buy:
            buy.update({ i:1 })

        request.session['buy'] = buy

        return HttpResponseRedirect("/cart/")
    except:
        return Message(request.META.get('HTTP_REFERER',"/")).autoRedirect(1).title('错误').message('当前商品不存在!').printMsg()

def clear(request, i):
    if not request.session.get('buy'):
        request.session["buy"] = {}

    data = {}
    try:
        buy = request.session["buy"]

        if i in buy:
            del buy[i]

        request.session['buy'] = buy

        return HttpResponseRedirect("/cart/")
    except:
        return Message(request.META.get('HTTP_REFERER',"/")).autoRedirect(1).title('错误').message('当前商品不存在!').printMsg()


def consignee(request):

    return render_to_response('consignee.htm', locals(), context_instance=RequestContext(request))



class Cart:
    """docstring for Cart"""
    def __init__(self, request):
        self.itemBuy = []
        self.countFee = 0
        self.itemQueryset = Item.objects.select_related().filter( \
                            Q(onLine=True) | \
                            Q(show=True))
        if request.session.get('buy'):
            for v, i in request.session['buy'].items():
                try:
                    item = Item.objects.getTagByItemFeeId(id='%s' % v)

                    subtotal = item.itemattr_set.amount * i
                    self.countFee += subtotal
                    self.itemBuy.append({ 'item': item, 'num': i,'subtotal': subtotal, 'v': v })
                except:
                    pass