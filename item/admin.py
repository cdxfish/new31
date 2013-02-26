#coding:utf-8
from django.contrib import admin
from models import *

admin.site.register(Item)
admin.site.register(ItemAttr)
admin.site.register(ItemDiscount)
admin.site.register(ItemFee)