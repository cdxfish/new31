#coding:utf-8
u"""日志"""
from django.shortcuts import render_to_response
from django.template import RequestContext
# Create your views here.

def log(request):
    u"""日志"""

    return render_to_response('item.htm', locals(), context_instance=RequestContext(request))