#coding:utf-8
from functools import wraps
# Create your decorator here.

# AJAX提示用
def ajaxMsg(msg):
    def _func(func):
    	@wraps(func)
        def __func(request, *args, **kwargs):
            try:
                return func(request, *args, **kwargs)

            except:
                from views import AjaxRJson

                return AjaxRJson().message(msg).dumps()
        return __func
    return _func