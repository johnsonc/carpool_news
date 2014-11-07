"""
WSGI config for carpool_news project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'carpool_news'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carpool_news.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
