#coding:utf-8

class FncMiddleware:

    def process_request(self, request):
        from views import FncSess
        
        FncSess(request).frMtSess()

        return None

    # def process_response(self, request, response):
    #     pass