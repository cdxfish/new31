#coding:utf-8

class UserMiddleware:

    def process_request(self, request):
        from models import BsInfo

        BsInfo.objects.frMt(request)

        return None