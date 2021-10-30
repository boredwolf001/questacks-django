"""
WSGI config for questacks questacks.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoquestacks.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questacks.settings')

application = get_wsgi_application()
