#coding:utf-8
u"""折扣"""
from django.shortcuts import render_to_response
from django.template import RequestContext
# Create your views here.

def dis(request):
    u"""折扣管理"""

    return render_to_response('specadmin.htm', locals(), context_instance=RequestContext(request))    