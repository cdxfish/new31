#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q, Min
from account.views import UserInfo
import random, json, os

# Create your views here.

def base(request):
    """
    加载APP For Office 基本信息类
    """
    if hasattr(request, 'base'):
        base = request.base
    else:
        request.base = BaseOffice()

    return {}


class BaseOffice:
    """docstring for Base"""

    actionTool = False

    def __init__(self):
        pass


class Purview:
    """权限"""
    def check(self,request, appName):
        
        return self.isStaff(request, appName)

    def isStaff(self,request, appName):

        if request.user.is_authenticated() and request.user.is_staff :
            
            return self.isPurview(request, appName)

        else:
            return HttpResponseRedirect("/account/login/")

    def isPurview(self,request, appName):

        userPurview = UserInfo(request.user).purview().returnPurview()

        if request.path in userPurview:
            return appName(request)
        else:
            return HttpResponseRedirect("/account/login/")