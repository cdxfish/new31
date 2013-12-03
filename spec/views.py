#coding:utf-8
u"""规格"""
from django.shortcuts import render_to_response
from django.template import RequestContext
# Create your views here.

def spec(request):
    u"""规格"""
 
    return render_to_response('specadmin.htm', locals(), context_instance=RequestContext(request))    