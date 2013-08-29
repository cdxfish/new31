#coding:utf-8
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect
import math, random, datetime


# 格式化价格,舍弃小数位
def frMtFee(fee):
    return math.floor(fee)

def keFrmt(fee):
    return math.floor(fee / 100) * 100 + 50 if fee % 100 < 50 else math.ceil(fee / 100) * 100

# 重定向至登录页
def rdrtLogin(request):
    return HttpResponseRedirect(request.nPath[u'登录'])

# 重定向至用户中心
def rdrtAcc(request):
    return HttpResponseRedirect(request.nPath[u'用户中心'])


# 重定向至首页
def rdrtIndex():
    return HttpResponseRedirect('/')


# 重定向至前一页
def rdrtBck(request):

    return HttpResponseRedirect(request.META.get('HTTP_REFERER',"/"))


# 分页
def page(l, p=1, pSize=150):

    p = int(p) if int(p) > 0 else 1
    paginator = Paginator(l, pSize)

    paginator.p = p

    try:
        return paginator.page(p)
    except (EmptyPage, InvalidPage):
        return paginator.page(paginator.num_pages)


# 排序方法
def sort(i):
    random.shuffle(i)
    return i


def rdrRange(url,date,sn):
    d = datetime.datetime.strptime(date, "%Y-%m-%d")
    s = d - datetime.timedelta(days=1)
    e = d + datetime.timedelta(days=1)

    return HttpResponseRedirect(u'%s?o=-1&c=-1&s=%s&e=%s&k=%s' % (url, s.strftime('%Y-%m-%d').strip(), e.strftime('%Y-%m-%d').strip(), sn))


def f02f(i):

    return '%0.2f' % i

def frmtDate(date):
    d = date.split('-')
    return datetime.date(int(d[0]), int(d[1]), int(d[2]))


def Patterns(*urls):
    """
        格式化全局url路由策略
        urls = (r'xxx', name, func, chcs, typ)
        chcs = ((0, u'json'), (1, u'查'), (2, u'增'), (3, u'删'), (4, u'改'), )
        typ = ((0, u'公共'), (1, u'私有'))
    """
    from django.conf.urls import patterns, url


    _urls = ( {'regex':i[0], 'view':i[1], 'name':i[1].func_name} for i in urls )

    return patterns('', *( url(**i) for i in _urls ) )