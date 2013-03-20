#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
import models, random, json, os


# Create your views here.

def tag(request, tagTitle = ''):
    # tagList = Tag().getTagByTag(tag).tagList
    tagList = Tag().getTagByItemName(itemName=tagTitle).tagList

    try:
        itemList = models.Item.objects.get(itemName=tagTitle).itemimg_set.all()
    except models.Item.DoesNotExist:
        itemList = Tag().getItemByTagTitle(tagTitle)



    return render_to_response('tag.htm', locals(), context_instance=RequestContext(request))

def tagAdmin(request):

    tagList =  models.Tag.objects.allTag()

    return render_to_response('tagadmin.htm', locals(), context_instance=RequestContext(request))


class Tag:
    """标签相关操作类"""

    def __init__(self):
        self.tagList = []
        self.color = ['DD9797','BA5252','D97D0F','E3BA9B','71BFCD','95BADD','A7CF50',]

    def random(self, num = 8):
        self.tagList = models.Tag.objects.randomTag(num)

        return self

    def tintTag(self, color = []):
        if not color: color = self.color
        for i in self.tagList:
            i.colorClass = random.choice(color)

        return self

    def getTagByTag(self, tag = '', num = 1):
        if tag: self.tagList = models.Tag.objects.getByTag(tag, num)

        if not self.tagList: self.getTagByItemName(tag, num)
   
        if not self.tagList: self.random(num)

        return self

    def getTagByItemName(self, itemName = '', num = 1):
        try:
            self.tagList =  models.Item.objects.select_related().get(itemName=itemName).tag_set.all()[: num]

        except models.Item.DoesNotExist:
            self.tagList = models.Tag.objects.getByTag(itemName, num)

        if not self.tagList: self.random(num)

        return self

    def getItemByTagTitle(self, tagTitle = ''):
        # try:
        #     self.tagList =  models.Item.objects.select_related().get(itemName=itemName).tag_set.all()[: num]

        # except models.Item.DoesNotExist:
        #     self.tagList = models.Tag.objects.getByTag(itemName, num)

        # if not self.tagList: self.random(num)

        return self