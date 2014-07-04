import sae
from new31 import wsgi

# application = sae.create_wsgi_app(wsgi.application)

from sae.ext.shell import ShellMiddleware


application = sae.create_wsgi_app(ShellMiddleware(wsgi.application, 'admin-new31'))