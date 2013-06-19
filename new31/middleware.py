#coding:utf-8

class new31Middleware:

    def process_request(self, request):

        for i,v in request.GET.items():
            request.GET[i] = v.strip()

        for i,v in request.POST.items():
            request.POST[i] = v.strip()

        for i,v in request.REQUEST.items():
            request.REQUEST[i] = v.strip()

        return None

    # def process_response(self, request, response):
    #     pass