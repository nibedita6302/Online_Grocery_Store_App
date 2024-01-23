from celery import Celery
from flask import current_app as app

celery = Celery('Online Grocery App Jobs')

class ContextTask(celery.Task):
    def __init__(self,*args,**kwargs):
        with app.app_context():
            return self.run(*args,**kwargs)
