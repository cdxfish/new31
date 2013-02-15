from django.conf.urls import patterns, include, url
from django.conf import settings
from views import *
import os.path

urlpatterns = patterns('',
    (r'^$', hello),
)

