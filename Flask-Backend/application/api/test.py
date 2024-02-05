from ..jobs import task
from flask import current_app as app

@app.route('/test',methods=['GET','POST'])
def test_celery_func():
    job = task.download_product_csv.delay()
    return str(job), 200