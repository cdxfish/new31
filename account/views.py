#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.http import HttpResponseRedirect
from account.models import *
from shop.common import *
import json

# Create your views here.

def login(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect("/")
            else:
                # Show an error page
                return Message().info('错误').message('用户名或密码错误!').printMsg()

        else:
            return render_to_response('login.htm')

    else:
        return HttpResponseRedirect("/")

def logout(request):

    auth.logout(request)

    return HttpResponseRedirect("/")

def settings(request):

    return render_to_response('settings.htm', locals())

def changepwd(request):

    return render_to_response('changepwd.htm', locals())

def orderList(request):

    return render_to_response('orderlist.htm', locals())

def orderDetail(request,x):

    return render_to_response('orderdetail.htm', locals())