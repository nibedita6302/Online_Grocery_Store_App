from celery import Celery
from flask import current_app as app

celery = Celery('Online Grocery App Jobs')

# Create a subclass of the task 
# that wraps the task execution in an application context.
# So its available               

# from .task.requestCategory import *
# from .task.sendEmail import *

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)
