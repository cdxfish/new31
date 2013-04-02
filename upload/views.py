#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from models import *

# Create your views here.

def specAdmin(request):
    specList = Spec.objects.select_related().all()

    return render_to_response('specadmin.htm', locals(), context_instance=RequestContext(request))    