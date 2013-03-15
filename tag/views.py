#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def tag(request):

    return render_to_response('tag.htm', locals(), context_instance=RequestContext(request))

def tagAdmin(request):

	return render_to_response('tagadmin.htm', locals(), context_instance=RequestContext(request))