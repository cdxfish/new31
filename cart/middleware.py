#coding:utf-8
from views import *
import datetime


class CartMiddleware:

    def process_request(self, request):

        if not 'itemCart' in request.session:
            request.session["itemCart"] = {}

        if not 'c' in request.session:
            request.session['c'] = ShipConsignee(request).c


        toDay = time.gmtime()
        cDate = time.strptime(request.session['c']['signDate'], '%Y-%m-%d')

        if cDate < toDay or not request.session['c']['signDate']:
            request.session['c']['signDate'] = '%s' % datetime.date.today()

        return None

    # def process_response(self, request, response):
    #     pass