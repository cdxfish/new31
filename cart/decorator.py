# coding: UTF-8
from django.contrib import messages
from new31.func import rdrtBck
from functools import wraps

# Create your decorator here.

# 商品下架装饰器
def itemshow(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        try:

            from item.models import ItemSpec
            ItemSpec.objects.get(id=kwargs['sid'], onl=True, show=True)

            return func(request, *args, **kwargs)

        except Exception, e:
            messages.warning(request, u'当前商品已下架')

            return rdrtBck(request)

    return _func


# 购物车检测用装饰器
def checkCartDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from views import CartSess

        if not CartSess(request).show()['items']:

            messages.warning(request, u'购物车内无商品')

            return rdrtBck(request)

        return func(request, *args, **kwargs)

    return _func