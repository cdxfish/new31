#coding:utf-8

from django.http import HttpResponse
from purview.views import *


class purviewMiddleware:
    """ 
    	后台页面入口保安
    	所有已注册的后台页面先经过此中间件的判定是否具有进入权限

    """

    def process_request(self, request):

        return Purview(request).check()