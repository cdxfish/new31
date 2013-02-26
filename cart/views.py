#coding:utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import datetime

# Create your views here.

def cart(request):
    now = datetime.datetime.now()

    return render_to_response('cart.htm', locals())

def consignee(request):
    now = datetime.datetime.now()

    return render_to_response('consignee.htm', locals())