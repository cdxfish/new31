#coding:utf-8
u"""票据打印"""
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def printOrd(request):
    u"""票据打印"""
    from logistics.forms import LogcSrchFrm
    from logistics.views import LogcsSerch, KpChng, sortList

    o = LogcsSerch(request)

    oList = o.get()
    oList = KpChng(oList, request).get()

    form = LogcSrchFrm(initial=o.initial)

    return render_to_response('printord.htm', locals(), context_instance=RequestContext(request))