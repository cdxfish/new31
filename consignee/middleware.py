#coding:utf-8
from views import *

class consigneeMiddleware:

    def process_request(self, request):

        ShipConsignee(request).formatConsignee()

        return None

    # def process_response(self, request, response):
    #     pass