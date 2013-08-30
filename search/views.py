#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def search(request):
    u"""搜索"""

    return render_to_response('search.htm', locals(), context_instance=RequestContext(request))