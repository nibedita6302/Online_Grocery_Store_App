import os
import shutil
from datetime import datetime
from flask import current_app as app
from application.jobs.workers import celery
from application.data.database import db
from application.data.models.inventory import Category
from application.data.models.users import Logs
from application.data.models.requests import RequestOnCategory
from celery.schedules import crontab
print('crontab',crontab)

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/5'), 
            implementRequest.s(), name='Implement Category Requests Every 5 minutes')

@celery.task()
def test():
    return 'Test Run Successfull!'

@celery.task()
def implementRequest():
    requests = RequestOnCategory.query.filter_by(status=1).all()
    # print('Fetching Requests',requests)
    if requests==[]:
        return 'No Approved Requests Yet!'
    for r in requests:
        if r.action == 'POST':
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
            if c1.prodct_count>0:
                return 'Unable to Delete!'
            db.session.delete(c1)
            log = Logs(user_id=r.requester, action='DELETE', table_name='category',
                        action_on=r.c_id, date=datetime.now(), is_admin=True)
            r.status = 2          # Implemented
            db.session.add(log)            
            db.session.commit()
    return 'All Processed!'
