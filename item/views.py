#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def item(request):

    return render_to_response('item.htm', locals(), context_instance=RequestContext(request))