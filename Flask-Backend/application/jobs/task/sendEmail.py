import os
from datetime import datetime, date
from flask import current_app as app
from ...jobs.workers import celery
from ...data.database import db
from ...data.models.shopping import Transaction
from ...data.models.users import Users
from ...jobs.setupEmail import sendEmail 
from ...data.models.requests import RequestOnCategory
from celery.schedules import crontab
# print('crontab',crontab)

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute=0, hour=16), 
            send_customer_reminder.s(), name='Send Customer Reminder everyday at 4pm')
    
    sender.add_periodic_task(crontab(0, 16, day_of_month='25'), 
            send_monthly_report.s(), name='Send Monthly Report to Admin at on 25th\
                                             of every month at 4pm')

@celery.task()
def send_customer_reminder():
    # send daily customer reminder is no activity
    trans = Transaction.query.all()
    print(trans)
    for t in trans:
        if datetime.strptime(t.bought_date, "%Y-%m-%\d %H:%M:%S.%/f").date() == date.today():
            print(t.user_id, t.bought_date) 
            user = Users.query.get(t.user_id)
            sendEmail(reciever_email=user.email)
    return 'All emails sent'


@celery.task()
def send_monthly_report():
    # send monthly report to admin
    sendEmail(receiver_email='nibedita.6302@gmail.com', email_type='report')
    return 'Monthly Report Communicated!'


@celery.task()
def download_product_csv():
    # download products csv for store manager 
    return 'message'