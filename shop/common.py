#coding:utf-8
from django.shortcuts import render_to_response

class Message:
    info ='hello world'
    message ='hello world'

    def info(self,info=''):
        self.info = info

        return self

    def message(self,message=''):
        self.message = message

        return self

    def printMsg(self):
        from django.shortcuts import render_to_response

        return render_to_response('message.htm', {'info': self.info, 'message': self.message})


class Shop:
    title = '我什么都不知道'

    def title(self, title):
        self.title = title

        return self