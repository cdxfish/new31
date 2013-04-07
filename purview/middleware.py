#coding:utf-8

from django.http import HttpResponse
from account.views import UserInfo
from purview.views import Ation


class ActionMiddleware:

    def process_request(self, request):

        request.action = Ation().action()


        return None

    # def process_response(self, request, response):
    #     pass