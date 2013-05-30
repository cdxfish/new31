#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages

# Create your views here.

def msg(request):

    return render_to_response('message.htm', locals(), context_instance=RequestContext(request))

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

class Message:
    def __init__(self, request):
        self.request = request
        self.auto = False

        self.redirectUrl = '/'

        self.formatMsg = {
                            'extendsHtm': 'shop.base.htm',
                            'auto': '',
                            'redirectUrl': '',
                        }

    def redirect(self, speed = 3, url=''):
        self.auto = speed

        # if url and (self.request.META.get('HTTP_REFERER',"/") != url):
        if url:
            self.redirectUrl = url
        else:
            self.redirectUrl = '/'


        return self

    def info(self,m=''):
        messages.info(self.request, m)

        return self

    def error(self,m=''):
        messages.error(self.request, m)

        return self

    def success(self,m=''):
        messages.success(self.request, m)

        return self    
           
    def warning(self,m=''):
        messages.warning(self.request, m)

        return self       
        
    def debug(self,m=''):
        messages.debug(self.request, m)

        return self

    def shopMsg(self):
        return self.msg('shop')

    def officeMsg(self):

        return self.msg('office')


    def msg(self, tempName= 'shop'):
        msg = self.formatMsg

        msg['extendsHtm'] = "%s.base.htm" % tempName
        msg['auto'] = self.auto
        msg['redirectUrl'] = self.redirectUrl

        self.request.session['msg'] = msg

        return HttpResponseRedirect('/message/')