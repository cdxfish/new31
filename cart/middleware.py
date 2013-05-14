#coding:utf-8
from views import *
import datetime, time


class cartMiddleware:

    def process_request(self, request):

    	Cart(request).setSeesion()

        return None

    # def process_response(self, request, response):
    #     pass