#coding:utf-8
# Create your views here.
from django.shortcuts import render_to_response
from shop.common import *

def tag(request):

    return render_to_response('tag.htm', locals())

def returnFrist(request):
    return HttpResponseRedirect("../")