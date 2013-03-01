#coding:utf-8
# Create your views here.
from django.shortcuts import render_to_response
import common, random, json


def shop(request, a):

    boxList = a

    return render_to_response('shop.htm', locals())
    # return HttpResponse(json.dumps(boxList))

def returnFrist(request):
    return HttpResponseRedirect("../")



def randBox():
    boxList = []
    for i in range(1, 10):
        int(random.uniform(1,23))
        a = {'class':'b1','name':'xiangnong','img':'/m/3133001s.jpg'}
        b = {'class':'b1','name':'xiangnong','img':'/m/3133011s.jpg'}
        c = {'class':'b2','name':'xiangnong','img':'/m/3133001b.jpg'}
        box = [a, b, c]

        random.shuffle(box)
        
        boxList.append(box)

    return boxList