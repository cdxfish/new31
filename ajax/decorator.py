#coding:utf-8

# Create your decorator here.

# AJAX提示用
def ajaxMsg(msg):
    def _func(func):
        def __func(request):
            try:
                return func(request)

            except:
                from views import AjaxRJson

                return AjaxRJson().message(msg).dumps()
        return __func
    return _func