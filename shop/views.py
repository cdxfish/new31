#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
import random
from new31.func import f02f

# Create your views here.

# APP For Shop UI
def shop(request):
    u"""商城首页"""
    from tag.views import TagSrch
    from tag.models import Tag
    from upload.models import Image
    from new31.func import sort

    items = ItemPin(10).getItems(sort)

    tags = Tag.objects.getByRandom()[:8]

    tagsCls = TagSrch.tagsCls

    ad = Image.objects.getAll()

    return render_to_response('shop.htm', locals(), context_instance=RequestContext(request))



class ItemPin(object):
    """
        瀑布流物品排序类
        用于首页物品展示用
        可看作矩阵

        实例化参数: 

        rSize(行长度) = 1
        lSize(列长度) = ((2, 0), (1, 1))

        使用方法: ItemPin(10).getItems()

        方便前台ajax调用, 返回值为列表, 格式为.

        [
            {
                'name': 'xxx', 
                'fee': '￥ %0.2f', 
                'like': 123, 
                'src': 'http://xxxxxx.jpg',
                'typ': 0,
             },
            .............
            ,
            .............
            ,
        ]

    """
    def __init__(self, rSize=8, lSize=((2, 0), (1, 1))):
        self.rSize = rSize
        self.lSize = lSize

        from item.models import ItemImg
        self.itemQuery = ItemImg.objects.getShowSImgs()  #初始化物品序列
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


    def __getLItem(self, size, typ):
        count = 0
        items = []
        for x in xrange(10):
            if count == size:
                break
            else:
                i = self.random()
                if i.typ == typ:
                    count += 1
                    items.append(self.__item(i))

        return items


    def __item(self, i):
        try:
            fee = i.item.itemspec_set.default().itemfee_set.nomal().fee
        except Exception, e:
            fee = 9999

        return  {
            'name': i.item.name, 
            'fee': '￥ %s' % f02f(fee), 
            'like': i.item.like, 
            'src': i.img.url,
            'typ': i.typ,
        }

    def random(self):

        return random.choice(self.itemQuery)