#coding:utf-8
from django.contrib import admin
from models import *

admin.site.register(Item)
admin.site.register(ItemSpec)
admin.site.register(ItemDiscount)
admin.site.register(ItemFee)
admin.site.register(ItemImg)
admin.site.register(ItemDesc)