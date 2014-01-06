# coding: UTF-8
"""
Using Jinja2 with Django 1.2
Based on: http://djangosnippets.org/snippets/2063/

To use:
  * Add this template loader to settings: `TEMPLATE_LOADERS`
  * Add template dirs to settings: `JINJA2_TEMPLATE_DIRS`

If in template debug mode - we fire the template rendered signal, which allows
debugging the context with the debug toolbar.  Viewing source currently doesnt
work.

If you want {% url %} or {% csrf_token %} support I recommend grabbing them
from Coffin (http://github.com/dcramer/coffin/blob/master/coffin/template/defaulttags.py)
Note for namespaced urls you have to use quotes eg:
  {% url account:login %} => {% url "account:login" %}
"""
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from django.template import TemplateDoesNotExist, Origin, base, loader
from django.core import urlresolvers
from django.conf import settings
from django.utils import six
import jinja2, os, sys

class Template(jinja2.Template, base.Template):
    def __init__(self, *args, **kwarg):
        super(Template, self).__init__(*args, **kwarg)


    def render(self, context):
        # flatten the Django Context into a single dictionary.
        context_dict = {}
        for d in context.dicts:
            context_dict.update(d)
        if settings.TEMPLATE_DEBUG:
            from django.test import signals
            self.origin = Origin(self.filename)
            signals.template_rendered.send(sender=self, template=self, context=context)

        return super(Template, self).render(context_dict)


class Loader(loader.BaseLoader):
    """
    A file system loader for Jinja2.

    Requires the following setting `JINJA2_TEMPLATE_DIRS`
    """
    is_usable = True

    if not six.PY3:
        fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
    app_template_dirs = list(settings.TEMPLATE_DIRS)

    for app in settings.INSTALLED_APPS:
        try:
            mod = import_module(app)
        except ImportError as e:
            raise ImproperlyConfigured('ImportError %s: %s' % (app, e.args[0]))
        template_dir = os.path.join(os.path.dirname(mod.__file__), 'templates')
        if os.path.isdir(template_dir):
            if not six.PY3:
                template_dir = template_dir.decode(fs_encoding)
            app_template_dirs.append(template_dir)

    # Set up the jinja env and load any extensions you may have
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(tuple(app_template_dirs)),
        extensions=(
            'jinja2.defaulttags.URLExtension',
            'jinja2.defaulttags.CsrfTokenExtension',
        )
    )
    env.template_class = Template

    # These are available to all templates.
    env.globals['url_for'] = urlresolvers.reverse
    env.globals['MEDIA_URL'] = settings.MEDIA_URL
    env.globals['STATIC_URL'] = settings.STATIC_URL

    def load_template(self, template_name, template_dirs=None):

        try:
            template = self.env.get_template(template_name)
        except jinja2.TemplateNotFound:
            raise TemplateDoesNotExist(template_name)

        return template, template.filename
