#coding:utf-8
from django.shortcuts import render_to_response
from shop.common import *

# Create your views here.

def checkout(request, **kwargs):

    common = kwargs

    return render_to_response('checkout.htm', locals())

def returnFrist(request):
    return HttpResponseRedirect("../")