#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import *
from message.views import *
from forms import *
import datetime

# Create your views here.


def consignee(request):

    form = getForms(request)

    return render_to_response('consignee.htm', locals(), context_instance=RequestContext(request))


def cConsignee(request):
    try:
        ShipConsignee(request).saveConsignee()

        return HttpResponseRedirect("/consignee/")
    except:
        return Message(request).redirect().warning('无法保存收货人信息').shopMsg()


class ShipConsignee:
    """docstring for Consignee"""
    def __init__(self, request):
        self.request = request
        self.c = {'user':'', 'pay':0, 'ship':0, 'consignee':'', 'area': 0, 'address':'', 'tel':'', 'signDate': '%s' % datetime.date.today(), 'time': 0,'note':'',} 

    def setSeesion(self):

        s = self.request.session['c']

        for v,i in self.request.REQUEST.items():
            # 用于下拉框默认值,使得过滤器辨别为false
            if i == '0':
                s[v] = 0
            else:
                s[v] = i

        self.request.session['c'] = s

        return self


    def clearConsignee(self):
        self.request.session['c'] = self.c

        return self