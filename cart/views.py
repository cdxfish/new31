#coding:utf-8
from django.shortcuts import render_to_response
from shop.common import *

# Create your views here.

def cart(request):

    return render_to_response('cart.htm', locals())

def consignee(request):

    return render_to_response('consignee.htm', locals())