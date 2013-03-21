#coding:utf-8
from django.shortcuts import render_to_response
from account.views import UserInfo

# Create your views here.

def base(request):
    """
    加载APP For Shop 基本信息类
    """
    if hasattr(request, 'user'):
        request.user = UserInfo(request.user).newOrderCount().newMsgCount().allmsgCount().returnInfo()

    return {'tagsClass':['DD9797','BA5252','D97D0F','E3BA9B','71BFCD','95BADD','A7CF50',]}