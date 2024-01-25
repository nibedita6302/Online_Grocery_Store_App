import os
import shutil
import csv
from datetime import datetime, date
from flask import current_app as app
from .workers import celery
from ..data.database import db
from .setupEmail import sendEmail 
from ..data.models.inventory import Category, Products
from ..data.models.shopping import Transaction
from ..data.models.users import Users
from ..data.models.users import Logs
from ..data.models.requests import RequestOnCategory
from celery.schedules import crontab
print('crontab',crontab)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/15'), 
            implementRequest.s(), name='Implement Category Requests Every 5 minutes')
    
    sender.add_periodic_task(crontab(minute=30, hour=21), 
            send_customer_reminder.s(), name='Send Customer Reminder everyday at 4pm')
    
    sender.add_periodic_task(crontab(30, 21, day_of_month='25'), 
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
    prod = Products.query.all()
    data = [{
        'p_id': p.p_id,
        'p_name': p.p_name,
        'p_description' : p.p_description,
        'brand': p.brand,
        'p_qty' : p.p_qty,
        'unit': p.unit,
        'price' : p.price,
        'stock' : p.stock,
        'stock_remaining' : p.stock_remaining,
        'is_deleted': p.is_deleted,
        'c_id' : p.c_id,
        'creator': p.creator
    } for p in prod]

     # Define CSV file path
    count = len(os.listdir('./PDF_Report/'))
    csv_file_path = f'product_{count}.csv'

    # Write data to CSV file
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['p_id', 'p_name', 'p_description', 'brand', 'p_qty', 'unit', 'price', 'stock',
                      'stock_remaining', 'is_deleted', 'c_id', 'creator']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

    return csv_file_path

@celery.task()
def implementRequest():
    requests = RequestOnCategory.query.filter_by(status=1).all()
    # print('Fetching Requests',requests)
    if requests==[]:
        return 'No Approved Requests Yet!'
    for r in requests:
        if r.action == 'POST':
            if Category.query.filter_by(c_name=r.c_name).first() is None:
                return 'Unable to Create Category'
            latest_id = Category.query.order_by(Category.c_id.desc()).first().c_id
            # print('latest_id',latest_id)
            extension = '.'+(r.c_image).split('.')[-1]
            img_path = (r.c_name).lower()+'_'+str(latest_id+1)+extension
            # print('image path',img_path,r.c_name, extension)
            location = os.path.join(app.config['UPLOAD_FOLDER']+'pendingUpload/',r.c_image)
            destination = os.path.join(app.config['UPLOAD_FOLDER']+'upload/',img_path)
            print(destination,location)            
            c1 = Category(c_name=r.c_name, c_image=img_path)
            log = Logs(user_id=r.requester, action='POST', table_name='category',
                    action_on=latest_id+1, date=datetime.now(), is_admin=True) 
            
            if os.path.exists(location):
                shutil.move(location,destination)  
                r.status = 2          # Implemented   
                db.session.add(c1)
                db.session.add(log)            
                db.session.commit()
            else:
                raise FileNotFoundError('Image not found in pendingUpload/ folder - ',r.c_image)
        elif r.action == 'PUT':
            c1 = Category.query.get(r.c_id)
            log = Logs(user_id=r.requester, action='PUT', table_name='category',
                    action_on=r.c_id, date=datetime.now(), is_admin=True)
            if r.c_name!='':
                print(r.c_name)
                c1.c_name = r.c_name
            if r.c_image!='':
                print(r.c_image, 'image')
                extension = '.'+(r.c_image).split('.')[-1]
                img_path = (r.c_name).lower()+'_'+str(c1.c_id)+extension
                c1.c_image = img_path
                old_image = os.path.join(app.config['UPLOAD_FOLDER']+'upload/',img_path)
                location = os.path.join(app.config['UPLOAD_FOLDER']+'pendingUpload/',r.c_image)
                destination = os.path.join(app.config['UPLOAD_FOLDER']+'upload/',img_path)    
                print(destination,location,old_image)                        
                if os.path.exists(location):
                    shutil.move(location,destination)   
                    r.status = 2          # Implemented
                    db.session.add(log)            
                    db.session.commit()
                else:
                    raise FileNotFoundError('Either old_image or image to be upload, not found - ',r.c_image)
            
        else:       #DELETE
            c1 = Category.query.get(r.c_id)
            if c1.product_count>0:
                return 'Unable to delete category!'
            db.session.delete(c1)
            log = Logs(user_id=r.requester, action='DELETE', table_name='category',
                        action_on=r.c_id, date=datetime.now(), is_admin=True)
            r.status = 2          # Implemented
            db.session.add(log)            
            db.session.commit()
    
    return 'All Processed!'
