#coding:utf-8
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf.urls import patterns, url, include
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import math, random, datetime, re, importlib


# 格式化价格,舍弃小数位
def frMtFee(fee):
    return math.floor(fee)

def keFrmt(fee):
    return math.floor(fee / 100) * 100 + 50 if fee % 100 < 50 else math.ceil(fee / 100) * 100

# 重定向至登录页
def rdrtLogin(request):
    return HttpResponseRedirect(reverse('account:login'))

# 重定向至用户中心
def rdrtAcc(request):
    return HttpResponseRedirect(reverse('account:myOrd'))


# 重定向至首页
def rdrtIndex():
    return HttpResponseRedirect(reverse('shop:shop'))


# 重定向至前一页
def rdrtBck(request):

    return HttpResponseRedirect(request.META.get('HTTP_REFERER',reverse('shop:shop')))


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


def Patterns(apps):
    """全局URL路由策略注册"""

    return patterns('', *[ ( r'^%s\/' % i , include('%s.urls' % i, namespace=i, app_name=i ) ) for i in apps ])

def pPatterns(*urls):
    """
        格式化全局url路由策略
        urls = (r'xxx', func, name, typ)
        typ = ((0, u'公共json'), (1, u'私有json'), (2, u'公共web'), (3, u'私有web'))
    """
    _urls = []
    for i in urls:
        _url = url(regex=i[0], view=i[1], name=i[1].__name__)
        _url.chcs = 0 if i[2] < 2 else 1
        _url.typ = i[2] % 2
        _url.moduleName = importlib.import_module(i[1].__module__).__doc__
        _urls.append(_url)

    return patterns('', *_urls )

def resolves(patterns):
    path = [[],[]]
    for i in patterns:
        for ii in i.url_patterns:
            if ii.moduleName:
                doc = '%s: ' % ii.moduleName
            else:
                doc = '%s: ' % i.app_name
            if doc:
                doc += re.sub(r'(\n|\t)', '', ii.callback.__doc__)
            else:
                doc += ii.name
            path[ii.typ] += [('%s:%s' % (i.app_name, ii.name), doc, ii.chcs)]

    path[0].sort()
    path[1].sort()

    return tuple(path[0]), tuple(path[1])