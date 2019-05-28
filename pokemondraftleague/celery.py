
import celery
import socket
import os
app = celery.Celery('example')
 
if (socket.gethostname().find("local")>-1):
    from pokemondraftleague.base_settings import *
    #REDIS_URL=REDIS_URL
    REDIS_URL='redis://'
else:
    REDIS_URL=os.environ.get('REDIS_URL')
app.conf.update(BROKER_URL=REDIS_URL,CELERY_RESULT_BACKEND=REDIS_URL)

#app.autodiscover_tasks()
@app.task
def add(x, y):
    return x + y