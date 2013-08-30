#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def items(request):
    u"""商品"""

    return render_to_response('item.htm', locals(), context_instance=RequestContext(request))