#coding:utf-8
u"""票据打印"""
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def printOrd(request):
    u"""票据打印"""
    from logistics.forms import LogcSrchFrm
    from logistics.views import LogcsSerch, KpChng

    o = LogcsSerch(request)

    oList = o.get()
    oList = KpChng(oList, request).get()

    form = LogcSrchFrm(initial=o.initial)

    return render_to_response('printord.htm', locals(), context_instance=RequestContext(request))

def pAct(request, sn):
    u"""打印"""
    from order.models import Ord
    from produce.models import Pro

    o = Ord.objects.get(sn=sn)
    o.total = Pro.objects.getFeeBySN(sn)


    return render_to_response('print.htm', locals(), context_instance=RequestContext(request))

