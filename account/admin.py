#coding:utf-8
from django.contrib import admin
from models import *

admin.site.register(User)
admin.site.register(UserAddress)
admin.site.register(UserBalance)