#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def newindex(request):
    u"""31客首页"""

    return render_to_response('newidenx.htm', locals(), context_instance=RequestContext(request))


def newquery(request):
    u"""订单查询"""

    return render_to_response('newquery.htm', locals(), context_instance=RequestContext(request))

def newlogin(request):
    u"""登录"""

    return render_to_response('newlogin.htm', locals(), context_instance=RequestContext(request))

def newcart(request):
    u"""购物车"""

    return render_to_response('newcart.htm', locals(), context_instance=RequestContext(request))