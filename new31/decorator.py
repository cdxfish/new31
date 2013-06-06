#coding:utf-8

# Create your decorator here.

# 订单提交类提示用装饰器
def subFailRemind(s= ''):
    def _newfunc(func):
        def __newfunc(self, **kwargs):
            if not self.error:

                if settings.DEBUG:
                    return func(self, kwargs)

                else:
                    try:
                        func(self, kwargs)
                    except:
                        self.error = True
                        self.message =  m

                        return Message(request).redirect().error(s).officeMsg()

        return __newfunc
    return _newfunc


# AJAX提示用
def tryMsg(msg):

    def _tryMsg(func):

        def __tryMsg(request, **kwargs):
            if settings.DEBUG:

                return func(request, kwargs)

            else:
                try:

                    return func(request, kwargs)
                except:

                    return AjaxRJson().message(msg).jsonEn()

        return __tryMsg

    return _tryMsg


# 提交模式检测包装函数
def checkPOST(func):
    def _func(request):
        if request.method == 'POST':

            return func(request)

        else:
            return Message(request).redirect(url=url).warning('订单提交方式错误 !').shopMsg() 
    return _func



# 页面跳转提示用装饰器
def redirTryMsg(msg):

    def _redirTryMsg(func):

        def __redirTryMsg(request, **kwargs):
            if settings.DEBUG:

                return func(request, kwargs)

            else:
                try:

                    return func(request, kwargs)
                except:

                    return msg

        return __redirTryMsg

    return _redirTryMsg


# AJAX提示用装饰器
def tryMsg(msg):

    def _tryMsg(func):

        def __tryMsg(request, **kwargs):
            if settings.DEBUG:

                return func(request, kwargs)

            else:
                try:

                    return func(request, kwargs)
                except:

                    return AjaxRJson().message(msg).jsonEn()

        return __tryMsg

    return _tryMsg
