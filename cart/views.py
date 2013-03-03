#coding:utf-8
from django.shortcuts import render_to_response

# Create your views here.

def cart(request, template,**kwargs):

    common = kwargs

    return render_to_response('%s.htm' % template, locals())

def consignee(request, **kwargs):

    common = kwargs

    return render_to_response('consignee.htm', locals())
