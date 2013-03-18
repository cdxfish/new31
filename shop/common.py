#coding:utf-8
from django.shortcuts import render_to_response
from account.views import UserInfo

# Create your views here.

def base(request):
    """
    加载APP For Shop 基本信息类
    """
    if hasattr(request, 'user'):
        request.user = UserInfo(request.user).returnInfo()

    return {}