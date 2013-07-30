#coding:utf-8
from django.contrib import admin
from models import Element, Privilege, Role

admin.site.register(Element)
admin.site.register(Privilege)
admin.site.register(Role)