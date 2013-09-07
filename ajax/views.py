#coding:utf-8
u"""ajax"""
from decorator import ajaxMsg
from new31.func import sort, f02f, frMtFee
from new31.cls import AjaxRJson
from django.core.urlresolvers import reverse
# Create your views here.
    
@ajaxMsg('无法解析')
def reToURL(request):
    u"""Http解析"""

    return AjaxRJson().dumps({'url': reverse(request.GET.get('r', ''))})