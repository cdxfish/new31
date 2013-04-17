#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q, Min
import random, json, os, time

# Create your views here.

# APP For Shop UI

def orderList(request):

    c = request.GET.get('c') if request.GET.get('c') else 0
    s = request.GET.get('s')
    e = request.GET.get('e')
    k = request.GET.get('k') if request.GET.get('k') else ''
    p = request.GET.get('p') if request.GET.get('p') else 1

    return render_to_response('orderlist.htm', locals(), context_instance=RequestContext(request))