#coding:utf-8
from functools import wraps
from django.http import HttpResponse
# Create your decorator here.

# AJAX提示用
def ajaxMsg(msg):
    def _func(func):
    	@wraps(func)
        def __func(request, *args, **kwargs):
            try:
                return func(request, *args, **kwargs)

            except:
                from message.models import Msg

                return HttpResponse(Msg.objects.dumps(msg=msg))
        return __func
    return _func