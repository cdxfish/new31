# coding: UTF-8
u"""物料"""
from django.shortcuts import render_to_response
from django.template import RequestContext
# Create your views here.

def bom(request):
    u"""物料"""

    return render_to_response('produceui.htm', locals(), context_instance=RequestContext(request))