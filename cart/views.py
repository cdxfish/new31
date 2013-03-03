#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def cart(request):

    return render_to_response('cart.htm', locals(), context_instance=RequestContext(request))

def consignee(request):

    return render_to_response('consignee.htm', locals(), context_instance=RequestContext(request))