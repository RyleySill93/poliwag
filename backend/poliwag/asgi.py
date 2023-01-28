"""
ASGI config for poliwag project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from ddtrace.contrib.asgi import TraceMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poliwag.settings")

django_asgi_application = get_asgi_application()
application = TraceMiddleware(django_asgi_application)
