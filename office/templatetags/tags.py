#coding:utf-8
from django import template
from django.core.urlresolvers import reverse
register = template.Library()  


class oprerateTag(template.Node):
    def __init__(self, value):
        self.value = value

    def render(self, context):
        value = self.value.resolve(context, True) #获取标签解析的真实对象

        s = '<td nowrap="nowrap" align="center">'
        for i in value.action:
            s += '<a href="%s" class="button %s">%s</a>' % (reverse(i[2], kwargs={'sn': value.sn}), i[2], i[1])

        return s + '</td>'

@register.tag(name='optr')
def forOprerate(parser, token):
    tag_name, text_name = token.split_contents() #分解标签传递的token字符串

    value = parser.compile_filter(text_name)  

    return oprerateTag(value)