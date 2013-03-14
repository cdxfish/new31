#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q, Min
import random, json, os

# Create your views here.

# APP For Shop UI
def checkLogin(request, defName):

    if request.user.is_authenticated() and request.user.is_staff :

    	return defName(request)


    else:
    	return HttpResponseRedirect("/account/login/")




def office(request):

	return render_to_response('office.htm', locals(), context_instance=RequestContext(request))