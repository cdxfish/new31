# coding: UTF-8
from django.contrib import admin
from models import Article

class articleAdmin(admin.ModelAdmin):
    class Media:
        js = (
              '/static/js/tinymce/tinymce.min.js',
              '/static/js/tinymce/textareas.js',
         )

admin.site.register(Article, articleAdmin)