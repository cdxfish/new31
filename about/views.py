#coding:utf-8
u"""关于"""
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def about(request):
    u"""订购指南"""

    return render_to_response('about.htm', locals(), context_instance=RequestContext(request))