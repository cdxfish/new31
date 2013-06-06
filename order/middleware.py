#coding:utf-8

class OrderMiddleware:
    
    def process_request(self, request):
        from views import OrderSubmit

        OrderSubmit(request).formatOrderType()

        return None

    # def process_response(self, request, response):
    #     pass