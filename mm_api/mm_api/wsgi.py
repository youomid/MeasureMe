"""
WSGI config for mm_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

# standard library imports
import os

# third party imports
from django.core.wsgi import get_wsgi_application

# local imports

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mm_api.settings")

application = get_wsgi_application()
