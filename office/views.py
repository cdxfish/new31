# coding: UTF-8
u"""管理中心"""
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
    y = '%s' % (today - oneDay)
    area = request.user.attribution_set.getAreaName()

    o = Ord.objects.filter(logcs__area__in=area, ordlog__act__in=['order:submitOrd', 'order:editOrd', 'cart:submit']).distinct().order_by('status', '-sn')
    l = Logcs.objects.filter(area__in=area).order_by('status', '-ord__sn')
    p = Pro.objects.filter(ord__logcs__area__in=area).order_by('status', '-ord__sn')
    f = Fnc.objects.filter(ord__logcs__area__in=area).order_by('status', '-ord__sn')

    order = o.filter(ordlog__time__range=(s, e))
    logcs = l.filter(date=s)
    pro = p.filter(ord__logcs__date=s)
    fnc = f.filter(ord__logcs__date=s)

    yorder = o.filter(ordlog__time__range=(y, s))
    ylogcs = l.filter(date=y)
    ypro = p.filter(ord__logcs__date=y)
    yfnc = f.filter(ord__logcs__date=y)

    return render_to_response('office.htm', locals(), context_instance=RequestContext(request))