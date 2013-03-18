#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def message(request):

    return Message(request.META.get('HTTP_REFERER',"/")).autoRedirect(10). \
        title('每个保安都是哲学家。他们每天都在提出哲学界的三个终极问题：').message('“你是谁？” “你从哪里来？” “你要到哪里去？”').printMsg()


class Message:
    title ='Give Me Fire'
    message ='Hello World'

    speed = 3
    backUrl = '/'
    autoRedirect = False

    def __init__(self, url):
        if url:
            self.backUrl = url

    def autoRedirect(self, speed = 3):
        self.autoRedirect = True
        self.speed = speed

        return self

    def title(self,title=''):
        self.title = title

        return self

    def message(self,message=''):
        self.message = message

        return self

    def printMsg(self):
        from django.shortcuts import render_to_response

        return render_to_response('message.htm', \
            {'autoRedirect':self.autoRedirect, 'speed': self.speed, 'backUrl':self.backUrl, 'title': self.title, 'message': self.message})