#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def signtimeAdmin(request):

    return render_to_response('signtimeadmin.htm', locals(), context_instance=RequestContext(request))