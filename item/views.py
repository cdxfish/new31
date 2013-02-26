#coding:utf-8
from django.shortcuts import render_to_response
from shop.common import *

# Create your views here.

def item(request):

    return render_to_response('item.htm', locals())

def returnFrist(request):
    return HttpResponseRedirect("../")