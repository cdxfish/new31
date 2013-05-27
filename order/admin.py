#coding:utf-8
from django.contrib import admin
from models import *

admin.site.register(OrderInfo)
admin.site.register(OrderLog)
admin.site.register(OrderLineTime)
admin.site.register(OrderLogistics)
admin.site.register(OrderStatus)
admin.site.register(OrderPay)
admin.site.register(OrderShip)
admin.site.register(OrderItem)