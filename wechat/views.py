#coding:utf-8
u"""微信"""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import hashlib
# Create your views here.

def responseMsg(request):
    u"""微信消息入口"""

    return HttpResponse('responseMsg')


def checkSignature(request):
    u"""微信接入验证"""

    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    echoStr = request.GET.get('echostr')

    token = 'new31com'

    tmpList = [token,timestamp,nonce]
    tmpList.sort()

    tmpstr = '%s%s%s' % tuple(tmpList)

    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return HttpResponse(echoStr)
    else:
        return HttpResponse(None)


def wechatShowTag(request, tag):
    u"""微信客户端标签页"""
    from tag.views import tagShow


    return tagShow(request=request, tag=tag)

def queryOrd(request):
    u"""微信客户端订单查询"""
    from order.views import queryOrd

    return queryOrd(request)