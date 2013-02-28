#coding:utf-8
# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from account.models import *
from shop.common import *

def settings(request):

    return render_to_response('settings.htm', locals(), context_instance=RequestContext(request))

def changepwd(request):

    return render_to_response('changepwd.htm', locals(), context_instance=RequestContext(request))

def orderList(request):

    return render_to_response('orderlist.htm', locals(), context_instance=RequestContext(request))

def orderDetail(request,x):

    return render_to_response('orderdetail.htm', locals(), context_instance=RequestContext(request))