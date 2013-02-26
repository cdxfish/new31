#coding:utf-8
# Create your views here.
from django.http import Http404
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from shop.common import *
import datetime

def loginUI(request):
    now = datetime.datetime.now()

    return render_to_response('login.htm', locals())

def login(request):
    if request.method != 'POST':
        return msg.info('错误').message('未知名错误').printMsg()

    else:
        return msg.info(request.POST['UserName']).message(request.POST['Password']).printMsg()

def settings(request):
    now = datetime.datetime.now()

    return render_to_response('settings.htm', locals())

def changepwd(request):
    now = datetime.datetime.now()

    return render_to_response('changepwd.htm', locals())

def orderList(request):
    now = datetime.datetime.now()

    return render_to_response('orderlist.htm', locals())

def orderDetail(request,x):
    now = datetime.datetime.now()

    return render_to_response('orderdetail.htm', locals())