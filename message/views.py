#coding:utf-8
u"""消息"""
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def message(request):
    u"""消息推送"""

    return render_to_response('produceui.htm', locals(), context_instance=RequestContext(request))