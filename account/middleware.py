#coding:utf-8

from django.http import HttpResponse



class UserMiddleware:

    def process_request(self, request):
    	from views import *

        if hasattr(request, 'user'):
            request.user = UserInfo(request.user).newOrderCount().newMsgCount().allmsgCount().purview().returnInfo()

        return None

    # def process_response(self, request, response):
    #     pass