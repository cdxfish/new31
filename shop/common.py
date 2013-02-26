#coding:utf-8

class Shop:
    msg ="Hello comger"
    def title(self,info=''):
        return info


    def printError(self,title='', message=''):
        from django.shortcuts import render_to_response

        return render_to_response('error.htm', {'title': title, 'message': message})

shop = Shop()

class Message:
    info ="Hello comger"
    message ="Hello comger"

    def info(self,info=''):
        self.info = info

        return self

    def message(self,message=''):
        self.message = message

        return self

    def printMsg(self):
        from django.shortcuts import render_to_response

        return render_to_response('message.htm', {'info': self.info, 'message': self.message})

msg = Message()