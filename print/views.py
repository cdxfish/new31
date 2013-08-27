#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def prntOrd(request):
    from logistics.forms import LogcSrchFrm
    from logistics.views import LogcsSerch, KpChng, sortList

    o = LogcsSerch(request)

    oList = o.get()
    oList = KpChng(oList, request).get()

    # sList = sortList(oList, o.initial)

    form = LogcSrchFrm(initial=o.initial)

    return render_to_response('printord.htm', locals(), context_instance=RequestContext(request))