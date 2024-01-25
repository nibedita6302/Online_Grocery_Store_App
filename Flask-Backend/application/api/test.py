from ..jobs import task
from flask import current_app as app

@app.route('/test',methods=['GET','POST'])
def test_celery_func():
    job = task.test.delay()
    return str(job), 200