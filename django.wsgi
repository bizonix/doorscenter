import os, sys
path = '/home/admin/public_html/searchpro.name/web'  # os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)
path = '/home/admin/public_html/searchpro.name/web/doorscenter'  # os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'doorscenter.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
