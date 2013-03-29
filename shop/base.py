#coding:utf-8
from django.shortcuts import render_to_response
from account.views import UserInfo

# Create your function here.

def tagsClass(request):

    return {'tagsClass':['DD9797','BA5252','D97D0F','E3BA9B','71BFCD','95BADD','A7CF50',]}