#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from models import *
from signtime.models import *

# Create your views here.

def iUI(request):

    return render_to_response('inventoryui.htm', locals(), context_instance=RequestContext(request))