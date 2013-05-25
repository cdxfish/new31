#coding:utf-8

import datetime


class MessageMiddleware:

    def process_request(self, request):

        from views import *

        if not 'msg' in request.session:
            request.session['msg'] = Message(request).formatMsg

        if not request.user.is_authenticated():
            request.session['msg']['extendsHtm'] = 'shop.base.htm'

        return None

    # def process_response(self, request, response):
    #     pass