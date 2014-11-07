"""
WSGI config for carpool_news project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carpool_news.settings")

# For production
if 'OPENSHIFT_REPO_DIR' in os.environ:
    sys.path.append(os.path.join(
        os.environ['OPENSHIFT_REPO_DIR'], 'carpool_news'))

    virtenv = os.environ['OPENSHIFT_HOMEDIR'] + 'python/virtenv/'
    os.environ['PYTHON_EGG_CACHE'] = os.path.join(
        virtenv, 'lib/python2.7/site-packages')

    virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
    try:
        execfile(virtualenv, dict(__file__=virtualenv))
    except IOError:
        pass

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
