#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from models import *

# Create your views here.

def signtimeAdmin(request):
    signTime = SignTime.objects.select_related().all()

    return render_to_response('signtimeadmin.htm', locals(), context_instance=RequestContext(request))