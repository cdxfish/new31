#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime

# Create your views here.

# APP For Shop UI

def office(request):
    u"""管理中心"""
    from order.models import Ord
    from logistics.models import Logcs
    from produce.models import Pro
    from finance.models import Fnc

    today = datetime.date.today()
    oneDay = datetime.timedelta(days=1)

    s = '%s' % today
    e = '%s' % (today + oneDay)

    order = Ord.objects.filter(ordlog__time__range=(s, e) ).order_by('status')
    logcs = Logcs.objects.filter(date__range=(s, e)).order_by('status')
    pro = Pro.objects.filter(ord__logcs__date__range=(s, e)).order_by('status')
    fnc = Fnc.objects.filter(ord__logcs__date__range=(s, e)).order_by('status')

    return render_to_response('office.htm', locals(), context_instance=RequestContext(request))