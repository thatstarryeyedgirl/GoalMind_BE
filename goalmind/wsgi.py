"""
WSGI config for goalmind project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os, sys, traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goalmind.settings')
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    print("ERROR STARTING DJANGO APP:", e)
    traceback.print_exc()
    sys.exit(1)
