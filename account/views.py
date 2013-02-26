#coding:utf-8
# Create your views here.
from django.shortcuts import render_to_response
from shop.common import *

def loginUI(request):

    return render_to_response('login.htm', locals())

def login(request):
    if request.method != 'POST':
        return Message().info('错误').message('method = %s ' % request.method).printMsg()

    else:
        return Message().info(request.POST['UserName']).message(request.POST['Password']).printMsg()

def settings(request):

    return render_to_response('settings.htm', locals())

def changepwd(request):

    return render_to_response('changepwd.htm', locals())

def orderList(request):

    return render_to_response('orderlist.htm', locals())

def orderDetail(request,x):

    return render_to_response('orderdetail.htm', locals())