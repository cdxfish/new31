#coding:utf-8
from django.contrib import admin
from models import Element, Privilege, Role

class elementAdmin(admin.ModelAdmin):
    filter_horizontal = ('element',)

class privilegeAdmin(admin.ModelAdmin):
    filter_horizontal = ('user', 'privilege',)


admin.site.register(Element)
admin.site.register(Privilege, elementAdmin)
admin.site.register(Role, privilegeAdmin)