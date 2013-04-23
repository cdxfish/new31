#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

# Create your views here.

def message(request):

    return Message(request, request.META.get('HTTP_REFERER',"/")).autoRedirect(10). \
        title('每个保安都是哲学家。他们每天都在提出哲学界的三个终极问题：').message('“你是谁？” “你从哪里来？” “你要到哪里去？”').shopMsg()

class Message:
    def __init__(self, request, url):
        self.request = request
        self.msgTitle ='Give Me Fire'
        self.msg ='Hello World'

        self.speed = 3

        self.autoRe = False


        if url and (self.request.META.get('HTTP_REFERER',"/") != url):
            self.backUrl = url
        else:
            self.backUrl = '/'


    def autoRedirect(self, speed = 3):
        self.autoRe = True
        self.speed = speed

        return self

    def title(self,t=''):
        self.msgTitle = t

        return self

    def message(self,m=''):
        self.msg = m

        return self

    def shopMsg(self):
        return self.printMsg('shopmsg')

    def officeMsg(self):

        return self.printMsg('officemsg')


    def printMsg(self, tempName):

        autoRedirect = self.autoRe
        speed = self.speed
        backUrl = self.backUrl
        title = self.msgTitle
        message = self.msg

        return render_to_response('%s.htm' % tempName, locals(), context_instance=RequestContext(self.request))