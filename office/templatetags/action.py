#coding:utf-8
from django import template  
  
register = template.Library()  
  
class TestNode(template.Node):  
    def __init__(self):  
        pass  
  
    def render(self, context):  
        return "xxxxx"  
  
def test(parser, token):  
    return TestNode()  
  
register.tag('action', test)  