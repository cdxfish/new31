#coding:utf-8

class OrdMiddleware:
    
    def process_request(self, request):
        from views import Ord

        Ord(request).format()

        return None

    # def process_response(self, request, response):
    #     pass