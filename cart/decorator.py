#coding:utf-8
from django.contrib import messages
from new31.func import rdrtBck

# Create your decorator here.

# 商品下架装饰器
def itemshow(func):
    def _func(request):
        try:
            from item.models import ItemSpec
            ItemSpec.objects.get(id=request.GET.get('id'), onl=True, show=True)

            return func(request)
            
        except:
            messages.warning(request, u'当前商品已下架')

            return rdrtBck(request)

    return _func

       
# 购物车检测用装饰器
def checkCartDr(func):
    def _func(request):
        from views import CartSess

        cart = CartSess(request).show()

        if not cart['items']:

            messages.warning(request, u'购物车内无商品')

            return rdrtBck(request)

        return func(request)

    return _func