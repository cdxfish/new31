#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q, Min
import random, json, os

# Create your views here.

# APP For Shop UI

def office(request):

    return render_to_response('office.htm', locals(), context_instance=RequestContext(request))