#coding:utf-8
from django.shortcuts import render_to_response
from django.contrib import auth
from django.template import RequestContext
from django.http import HttpResponseRedirect
from account.models import *

# Create your views here.

def login(request):

    if not request.user.is_authenticated():
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect("/")
            else:
                # Show an error page
                return Message().info('错误').message('用户名或密码错误!').printMsg()

        else:
            return render_to_response('login.htm', locals(), context_instance=RequestContext(request))

    else:
        return HttpResponseRedirect("/")

def logout(request):

    auth.logout(request)

    return HttpResponseRedirect("/")

def settings(request):

    return render_to_response('settings.htm', locals(), context_instance=RequestContext(request))

def changepwd(request):

    return render_to_response('changepwd.htm', locals(), context_instance=RequestContext(request))

def myOrder(request):

    return render_to_response('orderlist.htm', locals(), context_instance=RequestContext(request))

def orderDetail(request, orderSn):

    return render_to_response('orderdetail.htm', locals(), context_instance=RequestContext(request))

class UserInfo:
    newOrder = 0
    newMessage = 0
    messageCount = 0

    def checkOrder(self):
        self.newOrder = 2
        return self.newOrder

    def checkMessage(self):
        self.newMessage = 1
        return self.newMessage

    def returnInfo(self):
        self.messageCount = self.checkOrder() + self.checkMessage()

        returnInfo = {'newOrder': self.newOrder, 'newMessage': self.newMessage, 'messageCount': self.messageCount, }

        return returnInfo