#coding:utf-8

class UserMiddleware:

    def process_request(self, request):
        from models import UserInfo

        UserInfo.objects.frMt(request)

        return None