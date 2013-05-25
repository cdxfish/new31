#coding:utf-8

class CartMiddleware:
    
    def process_request(self, request):
        from views import Cart

        Cart(request).formatItems()

        return None

    # def process_response(self, request, response):
    #     pass