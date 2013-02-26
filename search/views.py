#coding:utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
import datetime

# Create your views here.

def search(request):
    now = datetime.datetime.now()

    return render_to_response('search.htm', locals())

def returnFrist(request):
    return HttpResponseRedirect("../")