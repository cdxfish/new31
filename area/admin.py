# coding: UTF-8
from django.contrib import admin
from models import Area, Attribution

class areaAdmin(admin.ModelAdmin):
    filter_horizontal = ('area',)

admin.site.register(Area)
admin.site.register(Attribution)