#coding:utf-8

class tagMiddleware:

    def process_request(self, request):
        from django.template import add_to_builtins
        # Uncomment the next line to enable the jinja_tag as if defaulttags
        add_to_builtins('jinja2.jinja2_tag')

    # def process_response(self, request, response):
    #     pass