#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from models import *

# Create your views here.

def areaAdmin(request):
    # areaList = Spec.objects.select_related().all().order_by('id')
 
    return render_to_response('areaadmin.htm', locals(), context_instance=RequestContext(request))    