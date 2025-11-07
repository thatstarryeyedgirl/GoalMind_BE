"""
WSGI config for goalmind project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""


import os
import sys
import traceback

print("Starting WSGI...")

try:
    from django.core.wsgi import get_wsgi_application
except Exception as e:
    print(" Django WSGI import failed:", e)
    traceback.print_exc()
    sys.exit(1)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goalmind.settings')

try:
    application = get_wsgi_application()
    print(" WSGI loaded successfully")
except Exception as e:
    print(" Django app startup failed:", e)
    traceback.print_exc()
    sys.exit(1)

