#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q, Min
import random, json, os

# Create your views here.

# APP For Shop UI

def office(request):
    from order.models import Ord
    from logistics.models import Logcs
    from produce.models import Pro
    from finance.models import Fnc

    order = Ord.objects.all()
    logcs = Logcs.objects.getAll()
    pro = Pro.objects.getAll()
    fnc = Fnc.objects.getAll()

    return render_to_response('office.htm', locals(), context_instance=RequestContext(request))