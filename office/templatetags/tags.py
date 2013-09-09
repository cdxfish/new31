#coding:utf-8
from django import template
from django.core.urlresolvers import reverse
register = template.Library()  


class oprerateTag(template.Node):
    def __init__(self, value):
        self.value = value

    def render(self, context):
        value = self.value.resolve(context, True) #获取标签解析的真实对象

        s = '<td nowrap="nowrap" align="center"><span class="oprt">'
        if value.action:
            for i in value.action:
                s += '<a href="%s" class="button %s">%s</a>' % (reverse(i[2], kwargs={'sn': value.sn}), i[2].replace(':',''), i[1])
        else:
            s += '&nbsp;' 

        return s + '</span></td>'

@register.tag(name='oprt')
def forOprerate(parser, token):
    tag_name, text_name = token.split_contents() #分解标签传递的token字符串

    value = parser.compile_filter(text_name)  

    return oprerateTag(value)


class statusTag(template.Node):
    def __init__(self, value):
        self.value = value

    def render(self, context):
        value = self.value.resolve(context, True) #获取标签解析的真实对象

        s = '<td nowrap="nowrap" align="center"><span class="status">'

        s += '<span class="status_%s" id="ord%s">%s</span> | <span class="status_%s" id="fnc%s">%s</span>| <span class="status_%s" id="logcs%s">%s</span>' % (
                value.status,
                value.sn,
                value.get_status_display(),
                value.fnc.status,
                value.sn,
                value.fnc.get_status_display(),
                value.logcs.status,
                value.sn,
                value.logcs.get_status_display()
            )


        return s + '</span></td>'


@register.tag(name='status')
def forStatus(parser, token):
    tag_name, text_name = token.split_contents() #分解标签传递的token字符串

    value = parser.compile_filter(text_name)  

    return statusTag(value)