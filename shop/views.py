#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from new31.func import sort
from tag.models import Tag
import random

# Create your views here.

# APP For Shop UI
def shop(request):
    from tag.views import TagsObj
    try:
        items = ItemPin(10).getItems(sort)
    except Exception, e:
        pass

    tags = Tag.objects.all()[:8]

    tagsCls = TagsObj.tagsCls

    return render_to_response('shop.htm', locals(), context_instance=RequestContext(request))



class ItemPin(object):
    """
        瀑布流物品排序类
        用于首页物品展示用
        可看作矩阵

        实例化参数: 

        rSize(行长度) = 1
        lSize(列长度) = ((2, 188), (1, 379))

        使用方法: ItemPin(10).getItems()

        方便前台ajax调用, 返回值为列表, 格式为.

        [
            {
                'name': 'xxx', 
                'fee': '￥ %0.2f', 
                'like': 123, 
                'src': 'http://xxxxxx.jpg',
                'width': 123,
                'height': 123
             },
            .............
            ,
            .............
            ,
        ]

    """
    def __init__(self, rSize=8, lSize=((2, 188), (1, 379))):
        self.rSize = rSize
        self.lSize = lSize

        from item.models import ItemImg
        self.itemQuery = ItemImg.objects.getSImgs()  #初始化物品序列
        self.matrix = []

    def getItems(self, func):
 
        return self.__getRItem(self.rSize, func).matrix

    """
        矩阵竖坐标

        长度为rSize


    """
    def __getRItem(self, rSize, func):

        for x in xrange(rSize):

            self.matrix += func(self.getLItem(self.lSize))

        return self


    """
        矩阵横坐标

        长度为lSize

    """
    def getLItem(self, lSize):
        items = []
        for x,v in lSize:
            items  += self.__getLItem(x,v)

        return items

    def __getLItem(self, size, width):
        count = 0
        items = []
        for x in xrange(10):
            if count == size:
                break
            else:
                i = self.random()
                if i.img.width == width:
                    count += 1
                    items.append(self.__item(i))

        return items

    def __item(self, i):

        return  {
            'name': i.item.name, 
            'fee': '￥ %0.2f' % i.item.itemspec_set.getDefaultSpec().itemfee_set.getFeeByNomal().fee, 
            'like': i.item.like, 
            'src': i.img.url,
            'width': i.img.width,
            'height': i.img.height
        }

    def random(self):

        return random.choice(self.itemQuery)