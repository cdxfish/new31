#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import *
from forms import *
import datetime, time

# Create your views here.


def consignee(request):

    form = getForms(request)

    return render_to_response('consignee.htm', locals(), context_instance=RequestContext(request))


class SpCnsgn:
    """docstring for Consignee"""
    def __init__(self, request):
        self.request = request
        self.c = request.session.get('c')
        
        try:
            payID = Pay.objects.getDefault().id
        except:
            payID = 0

        try:
            areaID = Area.objects.getDefault().id
        except:
            areaID = 0

        try:
            signID = SignTime.objects.getDefault().id
        except:
            signID = 0
        
        self.cFormat = {
                            'user':'', 
                            'pay': payID, 
                            'ship':0, 
                            'consignee':'', 
                            'area': areaID, 
                            'address':'', 
                            'tel':'', 
                            'date': '%s' % datetime.date.today(), 
                            'time': signID,
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


    def clear(self):

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
        cDate = time.strptime(c['date'], '%Y-%m-%d')

        if cDate < toDay or not c['date']:
            c['date'] = '%s' % datetime.date.today()


        return self.setConsignee(c)

    def setSiessionByOrd(self, sn):
        c = self.cFormat.copy()

        oLogcs = OrdInfo.objects.get(sn=sn).ordlogcs

        orderPay = oLogcs.ord.ordpay

        try:
            pay = Pay.objects.get(name=orderPay.payName, cod=orderPay.cod).id
        except Exception, e:
            pay = Pay.objects.getDefault().id

        areaList = oLogcs.area.split(' - ')


        try:
            area = Area.objects.get(name=areaList[1]).id
        except Exception, e:
            area = Area.objects.getDefault().id


        try:
            time = SignTime.objects.get(stime=oLogcs.start, etime=oLogcs.end).id
        except Exception, e:
            time = SignTime.objects.getDefault().id



        c['user'] = oLogcs.ord.user
        c['pay'] = pay
        c['consignee'] = oLogcs.consignee
        c['area'] = area
        c['address'] = oLogcs.address
        c['tel'] = oLogcs.tel
        c['date'] = '%s' % oLogcs.date

        c['time'] = time
        c['note'] = oLogcs.note

        return self.setConsignee(c)
