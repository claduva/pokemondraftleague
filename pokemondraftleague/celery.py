from __future__ import absolute_import, unicode_literals
import django
import os
import socket
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pokemondraftleague.settings')

app = Celery('example')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

#configure redis 
if (socket.gethostname().find("local")>-1):
    from pokemondraftleague.base_settings import *
    REDIS_URL='redis://'
else:
    REDIS_URL=os.environ.get('REDIS_URL')
app.conf.update(BROKER_URL=REDIS_URL,CELERY_RESULT_BACKEND=REDIS_URL)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()