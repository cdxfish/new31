#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages

# Create your views here.

def msg(request):

    return render_to_response('message.htm', locals(), context_instance=RequestContext(request))

class Message:
    def __init__(self, request):
        self.request = request
        self.auto = False

        self.redirectUrl = '/'

    def redirect(self, speed = 3, url=''):
        self.auto = speed

        if url and (self.request.META.get('HTTP_REFERER',"/") != url):
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


        msg = {
                'extendsHtm': "%s.base.htm" % tempName,
                'auto': self.auto,
                'redirectUrl': self.redirectUrl,
            }

        self.request.session['msg'] = msg

        return HttpResponseRedirect('/message/')