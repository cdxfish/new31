#coding:utf-8
from django import template

register = template.Library()  


class oprerateTag(template.Node):
    def __init__(self, value):
        self.value = value

    def render(self, context):
        value = self.value.resolve(context, True) #获取标签解析的真实对象

        s = '<td nowrap="nowrap" align="center">'
        for i,v in value.action.items():
            for ii,vv in v:
                try:
                    sn =  value.ord.sn
                    s += '<a href="%s%s/?sn=%s" class="button">%s</a>' % (i, ii, value.id, vv)
                except Exception, e:
                    s += '<a href="%s%s/?sn=%s" class="button">%s</a>' % (i, ii, value.sn, vv)

        return s + '</td>'

@register.tag(name='optr')
def forOprerate(parser, token):
    tag_name, text_name = token.split_contents() #分解标签传递的token字符串

    value = parser.compile_filter(text_name)  

    return oprerateTag(value)



# @register.filter(name='optr')
# @register.inclusion_tag('link.html', takes_context=True)
# def forOprerate(value):
#     s = ''
#     for i,v in value.action.items():
#         for ii,vv in v:
#           s += '<a href="%s%s/?sn=%s" class="button">%s</a>' % (i, ii, value.sn, vv)

#     return s