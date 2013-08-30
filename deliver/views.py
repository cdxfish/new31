#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def deliver(request):
    u"""物流方式管理"""

    return render_to_response('produceui.htm', locals(), context_instance=RequestContext(request))