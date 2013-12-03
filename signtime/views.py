#coding:utf-8
u"""收货时间"""
from django.shortcuts import render_to_response
from django.template import RequestContext
# Create your views here.

def signtime(request):
    u"""收货时间"""

    return render_to_response('signtimeadmin.htm', locals(), context_instance=RequestContext(request))