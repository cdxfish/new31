#coding:utf-8

import datetime


class CartMiddleware:

    def process_request(self, request):

        if not 'itemCart' in request.session:
            request.session["itemCart"] = {}

        if not 'c' in request.session:
            request.session['c'] = {'pay':0, 'ship':0, 'consignee':'', 'area': 0, 'address':'', 'tel':'', 'date': '%s' % datetime.date.today(), 'time': 0,'note':'',}

        return None

    # def process_response(self, request, response):
    #     pass