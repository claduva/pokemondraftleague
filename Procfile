web: gunicorn pokemondraftleague.wsgi
worker: celery worker -A pokemondraftleague -l info --loglevel=debug
worker: celery -A pokemondraftleague beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler