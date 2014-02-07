# coding: UTF-8

class OrdMiddleware:

    def process_request(self, request):
        from views import OrdSess

        OrdSess(request).frMt()

        return None

    # def process_response(self, request, response):
    #     pass