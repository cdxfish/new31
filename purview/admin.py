# coding: UTF-8
from django.contrib import admin
from models import EleSub, Element, Privilege, Role

class eleSubAdmin(admin.ModelAdmin):
    filter_horizontal = ('sub',)

class privilegeAdmin(admin.ModelAdmin):
    filter_horizontal = ('element',)

class roleAdmin(admin.ModelAdmin):
    filter_horizontal = ('user', 'privilege',)
    raw_id_fields = ('user',)


admin.site.register(Element)
admin.site.register(EleSub)
admin.site.register(Privilege, privilegeAdmin)
admin.site.register(Role, roleAdmin)