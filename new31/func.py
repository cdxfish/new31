#coding:utf-8
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect
import math, random, datetime


# 格式化价格,舍弃小数位
def forMatFee(fee):

    return math.floor(fee)


# 重定向至登录页
def redirectLogin():
    return HttpResponseRedirect("/account/login/")


# 重定向至首页
def redirect():
    return HttpResponseRedirect('/')


# 重定向至前一页
def rdrBck(request, L=[]):
    HTTP_REFERER = request.META.get('HTTP_REFERER',"/")

    if count():
        return HttpResponseRedirect(HTTP_REFERER)
    else:
        return redirect()

# 闭包计数器
def count():
    i = 0

    def _func(i):
        i +=  1
        return i

    if i:
        return _func
    else:
        return _func(i)


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
