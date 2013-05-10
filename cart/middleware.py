#coding:utf-8
from views import *
import datetime, time


class cartMiddleware:

    def process_request(self, request):

        if not 'itemCart' in request.session:
            request.session["cart"] = Cart.items

        return None

    # def process_response(self, request, response):
    #     pass