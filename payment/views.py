#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q, Min
from models import *

# Create your views here.

# APP For Shop UI

def payList(request):

	pay = Pay.objects.select_related().all()

	return render_to_response('paylist.htm', locals(), context_instance=RequestContext(request))