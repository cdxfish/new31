# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
import datetime

def hello(request):
    now = datetime.datetime.now()
    t = loader.get_template('shop.htm')
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)

def returnFrist(request):
    return HttpResponseRedirect("../")