# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import datetime

def hello(request):
    now = datetime.datetime.now()
    t = get_template('cart.htm')
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)