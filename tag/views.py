#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from item.models import Item


# Create your views here.

def tag(request, tagTitle = ''):

    # d = dir(Item)

    item = Item.objects.getItemByItemName(itemName=tagTitle)

    # try:
    #     item = models.Item.objects.getItemByItemName(itemName=tagTitle)
    # except models.Item.DoesNotExist:
    #     itemList = Tag().getItemByTagTitle(tagTitle)

    return render_to_response('tag.htm', locals(), context_instance=RequestContext(request))

def tagAdmin(request):

    tagList =  Tag().objects.allTag()

    return render_to_response('tagadmin.htm', locals(), context_instance=RequestContext(request))


class Tag:
    """标签相关操作类"""

    def __init__(self):
        self.tagList = []

    def random(self, num = 8):
        self.tagList = models.Tag.objects.randomTag(num)

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