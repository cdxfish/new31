# coding: UTF-8
from django.contrib import admin
from models import InvPro, InvNum, Build

class buildAdmin(admin.ModelAdmin):
    filter_horizontal = ('area', )

admin.site.register(InvPro)
admin.site.register(InvNum)
admin.site.register(Build, buildAdmin)