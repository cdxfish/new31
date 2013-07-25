#coding:utf-8

class CnsgnMiddleware:

    def process_request(self, request):
        from views import LogcSess
        
        LogcSess(request).frMt().chkDate()

        return None

    # def process_response(self, request, response):
    #     pass