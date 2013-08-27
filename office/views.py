#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q, Min
import datetime

# Create your views here.

# APP For Shop UI

def office(request):
    from order.models import Ord
    from logistics.models import Logcs
    from produce.models import Pro
    from finance.models import Fnc


    today = datetime.date.today()
    oneDay = datetime.timedelta(days=1)

    s = '%s' % today
    e = '%s' % (today + oneDay)

    order = Ord.objects.filter(ordlog__time__range=(s, e) )
    logcs = Logcs.objects.filter(date__range=(s, e))
    pro = Pro.objects.filter(ord__logcs__date__range=(s, e))
    fnc = Fnc.objects.filter(ord__logcs__date__range=(s, e))

    return render_to_response('office.htm', locals(), context_instance=RequestContext(request))