#coding:utf-8
# from views import *
class UserMiddleware:

    def process_request(self, request):
        from views import UserInfo
        
        if hasattr(request, 'user'):
            request.user = UserInfo(request.user).get()

        return None