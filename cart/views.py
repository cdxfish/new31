#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from item.models import *

# Create your views here.

def cart(request):
    cart = Cart(request)

    d = dir(ItemFee.objects.get(id='1').amount)

    return render_to_response('cart.htm', locals(), context_instance=RequestContext(request))

def buy(request, i):

    return render_to_response('cart.htm', locals(), context_instance=RequestContext(request))

def consignee(request):

    return render_to_response('consignee.htm', locals(), context_instance=RequestContext(request))



class Cart:
    """docstring for Cart"""
    def __init__(self, request):
        self.itemBuy = []
        for i,v in request.session['buy'].items():
            item = ItemFee.objects.get(id=i)
            self.itemBuy.append({ 'item': item, 'num': i,'subtotal': item.amount })