#coding:utf-8
from django import template
from django.core.urlresolvers import reverse
register = template.Library()  


class pageTag(template.Node):
    def __init__(self, value, request, form):
        self.value = value
        self.request = request
        self.form = form

    def render(self, context):
        u = self.value.resolve(context, True) #获取标签解析的真实对象
        request = self.request.resolve(context, True)
        form = self.form.resolve(context, True)

        k = u''
        for i in self.form.resolve(context, True):
            k += u'%s=%s&' % (i.name, i.value())

        s = u'<tr><td align="right" nowrap="true" colspan="10">总计 %s 条记录，共 %s 页，当前第 %s 页' % (u.paginator.count, u.paginator.num_pages, u.paginator.p)
        s += u'<span id="pageLink">'
        s += u'<a href="%s?%sp=1">第一页</a>' % (request.path, k)

        if u.has_previous():
            s += u'<a href="%s?%sp=%s">上一页</a>' % (request.path, k, u.previous_page_number())

        if u.has_next():
            s += u'<a href="%s?%sp=%s">下一页</a>' % (request.path, k, u.next_page_number())

        s +=  u'</span></td></tr>'

        return s

@register.tag(name='page')
def page(parser, token):
    tag, u, request, form = token.split_contents() #分解标签传递的token字符串

    return pageTag(parser.compile_filter(u), parser.compile_filter(request), parser.compile_filter(form))