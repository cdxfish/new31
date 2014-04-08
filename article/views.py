# coding: UTF-8
u"""关于"""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404

# Create your views here.

def article(request, tag):
    u"""文章页"""
    from models import Article

    alists = Article.objects.values('tag', 'title')
    try:
        article = Article.objects.get(tag=tag)
        return render_to_response('article.htm', locals(), context_instance=RequestContext(request))

    except Exception, e:
        raise Http404
