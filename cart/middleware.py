#coding:utf-8
from views import *
import datetime


class CartMiddleware:

    def process_request(self, request):

        if not 'itemCart' in request.session:
            request.session["itemCart"] = {}

        if not 'c' in request.session:
            request.session['c'] = ShipConsignee(request).c

        return None

    # def process_response(self, request, response):
    #     pass