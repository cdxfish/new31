#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
import models

# Create your views here.

def tag(request):

    return render_to_response('tag.htm', locals(), context_instance=RequestContext(request))

def tagAdmin(request):

  tagList = Tag().getTagAll().tagAllList

  return render_to_response('tagadmin.htm', locals(), context_instance=RequestContext(request))

def tagAdd(request):

  tagList = Tag().getTagAll().tagAllList

  return render_to_response('tagadd.htm', locals(), context_instance=RequestContext(request))


class Tag:
    """标签相关操作类"""
    def __init__(self):

       self.tagAllList = []

    # 获取全部标签
    def getTagAll(self):      
       	self.tagAllList = models.Tag.objects.allTag()

        return self
