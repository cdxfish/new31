#coding:utf-8

from django.http import HttpResponse
from account.views import UserInfo
from message.views import Message
from purview.views import *


class purviewMiddleware:
    """权限中间件"""

    def process_request(self, request):

		return Purview(request).check()