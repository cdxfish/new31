#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings 
from django.db.models import Q, Min
from item.models import Item
import random, json, os

# Create your views here.

# APP For Shop UI
def index(request):


    return render_to_response('office.htm', locals(), context_instance=RequestContext(request))