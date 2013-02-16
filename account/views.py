# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import datetime

def settings(request):
    now = datetime.datetime.now()
    t = get_template('settings.htm')
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)

def changepwd(request):
    now = datetime.datetime.now()
    t = get_template('changepwd.htm')
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)

def orderList(request):
    now = datetime.datetime.now()
    t = get_template('orderlist.htm')
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)
    
def orderDetail(request,x):
    now = datetime.datetime.now()
    t = get_template('orderdetail.htm')
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)