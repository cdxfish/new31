#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def payList(request):

	pay = Pay.objects.select_related().all()

	return render_to_response('paylist.htm', locals(), context_instance=RequestContext(request))