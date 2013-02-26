#coding:utf-8
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
import datetime

def tag(request):
    now = datetime.datetime.now()

    return render_to_response('tag.htm', locals())

def returnFrist(request):
    return HttpResponseRedirect("../")