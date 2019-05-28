from pokemondraftleague.celery import app

@app.task
def add(x, y):
    return x + y