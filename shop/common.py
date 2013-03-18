#coding:utf-8
from django.shortcuts import render_to_response
from account.views import UserInfo


class Message:
    info ='hello world'
    message ='hello world'

    def info(self,info=''):
        self.info = info

        return self

    def message(self,message=''):
        self.message = message

        return self

    def printMsg(self):
        from django.shortcuts import render_to_response

        return render_to_response('message.htm', {'info': self.info, 'message': self.message})


def base(request):
    """
    加载APP For Shop 基本信息类
    """
    if hasattr(request, 'user'):
        request.user = UserInfo(request.user).returnInfo()

    return {}