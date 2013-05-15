#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import *
from message.views import *
from forms import *
import datetime, time

# Create your views here.


def consignee(request):

    form = getForms(request)

    return render_to_response('consignee.htm', locals(), context_instance=RequestContext(request))


class ShipConsignee:
    """docstring for Consignee"""
    def __init__(self, request):
        self.request = request
        self.c = request.session['c']
        self.cFormat = {
                            'user':'', 
                            'pay':0, 
                            'ship':0, 
                            'consignee':'', 
                            'area': 0, 
                            'address':'', 
                            'tel':'', 
                            'signDate': '%s' % datetime.date.today(), 
                            'time': 0,
                            'note':'',
                        } 

    def setSeesion(self):
        s = self.c

        for v,i in self.request.REQUEST.items():
            # 用于下拉框默认值,使得过滤器辨别为false
            if i == '0':
                s[v] = 0
            else:
                s[v] = i

        return self.setConsignee(s)


    def clearConsignee(self):

        return self.setConsignee(self.cFormat)

    def setConsignee(self, c):
        self.request.session['c'] = c

        self.c = c

        return self

    def formatConsignee(self):
        if not self.c:

            self.setConsignee(self.cFormat)

        c = self.c

        toDay = time.gmtime()
        cDate = time.strptime(c['signDate'], '%Y-%m-%d')

        if cDate < toDay or not c['signDate']:
            c['signDate'] = '%s' % datetime.date.today()


        return self.setConsignee(c)