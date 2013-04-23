#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q, Min
from message.views import *
from models import *
import random, json, os, time,datetime

# Create your views here.

def orderList(request):

    c = request.GET.get('c') if request.GET.get('c') else 0
    s = request.GET.get('s')
    e = request.GET.get('e')
    k = request.GET.get('k') if request.GET.get('k') else ''
    p = request.GET.get('p') if request.GET.get('p') else 1

    return render_to_response('orderlist.htm', locals(), context_instance=RequestContext(request))

def orderSubmit(request):
    if request.method == 'POST':

        orderId = OrderCon(request).orderSubmit().orderId

        return Message(request, request.META.get('HTTP_REFERER',"/")).title('您已成功提交订单').message('感谢您在本店购物！请记住您的订单号: %d' % orderId).shopMsg()

    else:
        return Message(request, request.META.get('HTTP_REFERER',"/")).title('错误').message('订单提交错误 !').shopMsg()





class OrderCon:
    """docstring for Order"""
    def __init__(self, r):
        self.request = r
        self.orderId = 2013113082322
        # self.order = None

    def orderSubmit(self):

        # 新订单锁定、插入基本信息
        self.newOderSn().submitOrderInfo()

        return self


    # 获得新的订单编号
    def getNewOrderSn(self):
        t = time.gmtime()
        tCount = t.tm_hour * t.tm_min * t.tm_sec
        sExpiryDate = self.request.session.get_expiry_date()
        sCount = (sExpiryDate.hour * sExpiryDate.minute * sExpiryDate.second ) % 10

        return int('%d%d%05d%d' % (t.tm_year, t.tm_yday, tCount, sCount))


    # 锁定新订单进行订单号占位
    def newOderSn(self):

        self.orderId = self.getNewOrderSn()

        runOrder = True

        while runOrder:
            try:
                self.order = OrderInfo.objects.get(orderSn=self.orderId)

            except:
                runOrder = False

                self.order = OrderInfo(orderSn=self.orderId)

                self.order.save()
                
            else:
                self.orderId += 1

        return self

    # 插入订单基本信息
    def submitOrderInfo(self, u= '' , r ='网店订单'):

        self.order.referer=r
        self.order.user= u if u else self.request.user.username
        self.order.note= self.request.session['c']['note']

        self.order.save()


        return self