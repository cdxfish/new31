#coding:utf-8
from views import *
class UserMiddleware:

    def process_request(self, request):
        # from views import *

        if hasattr(request, 'user'):
            request.user = UserInfo(request.user).newOrderCount().newMsgCount().allmsgCount().returnInfo()

        return None