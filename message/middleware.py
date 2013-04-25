#coding:utf-8

import datetime


class MessageMiddleware:

    def process_request(self, request):

        if not 'msg' in request.session:
            request.session['msg'] = {
                                        'extendsHtm': 'shop.base.htm',
                                        'auto': '',
                                        'redirectUrl': '',
                                    }

        return None

    # def process_response(self, request, response):
    #     pass