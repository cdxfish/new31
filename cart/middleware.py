# coding: UTF-8

class CartMiddleware:

    def process_request(self, request):
        from views import CartSess

        CartSess(request).frMt()

        return None