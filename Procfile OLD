web: python manage.py process_tasks & gunicorn pokemondraftleague.wsgi
worker: celery worker -A pokemondraftleague -l info
processor: celery -A pokemondraftleague worker --beat --scheduler django_celery_beat.schedulers:DatabaseScheduler -l info
worker2: python discordbot/discordbot.py