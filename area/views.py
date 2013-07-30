#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def areaAdmin(request):
	from models import Area

    areaList = Area.objects.select_related().all().order_by('id')
 
    return render_to_response('areaadmin.htm', locals(), context_instance=RequestContext(request))    