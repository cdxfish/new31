#coding:utf-8


class ConsigneeMiddleware:

    def process_request(self, request):
        from views import *

        ShipConsignee(request).formatConsignee()

        return None

    # def process_response(self, request, response):
    #     pass