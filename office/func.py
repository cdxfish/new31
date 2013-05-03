#coding:utf-8
from django.core.paginator import Paginator, InvalidPage, EmptyPage

# Create your views here.

def page(l='', p=1, pSize=150):

    p = int(p) if int(p) > 0 else 1
    paginator = Paginator(l, pSize)

    try:
        return paginator.page(p)
    except (EmptyPage, InvalidPage):
        return paginator.page(paginator.num_pages)