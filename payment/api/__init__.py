#coding:utf-8
import payafter
import alipay
import post
import quarter
import monthly
import coupons
import ccbtransfer
import icbctransfer
import abctransfer
import points


class APIs(object):
    """docstring for APIs"""
    def __init__(self, ord, *args, **kwarg):
        self.ord = ord

        self.args = args
        self.kwarg = kwarg
        
    def payUrl(self):
        

        return '/'