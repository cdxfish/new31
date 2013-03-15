#coding:utf-8
from django.contrib import admin
from models import *

admin.site.register(OrderInfo)
admin.site.register(OrderItem)
admin.site.register(OrderAttr)
admin.site.register(OrderFee)
admin.site.register(OrderDiscount)