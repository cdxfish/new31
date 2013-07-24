#coding:utf-8

class CnsgnMiddleware:

    def process_request(self, request):
        from views import Cnsgn
        
        Cnsgn(request).frmtCnsgn()

        return None

    # def process_response(self, request, response):
    #     pass