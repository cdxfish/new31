#coding:utf-8
from django.contrib import admin
from models import Item, ItemSpec, ItemFee, ItemImg, ItemDesc

class ItemAdmin(admin.ModelAdmin):
    filter_horizontal = ('tag',)

admin.site.register(Item, ItemAdmin)
admin.site.register(ItemSpec)
admin.site.register(ItemFee)
admin.site.register(ItemImg)
admin.site.register(ItemDesc)