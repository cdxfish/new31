#coding:utf-8
u"""关于"""
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def about(request):
    u"""关于31客"""

    return render_to_response('about.htm', locals(), context_instance=RequestContext(request))

def guide(request):
    u"""订购指南"""

    return render_to_response('guide.htm', locals(), context_instance=RequestContext(request))
   
def ex(request):
    u"""K金换购"""

    return render_to_response('ex.htm', locals(), context_instance=RequestContext(request))

    
def pub(request):
    u"""大客户"""

    return render_to_response('pub.htm', locals(), context_instance=RequestContext(request))