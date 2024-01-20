import os
from datetime import datetime
from application.data.models.requests import *
from application.data.models.users import Users
from application.data.models.users import Logs
from flask_restful import Resource, fields, marshal, reqparse
from application.data.database import db
from flask import current_app as app
from flask import request
from flask_login import login_required, current_user
from flask_security import auth_required, roles_required, roles_accepted

request_fields = {
    "cn_id": fields.Integer,
    "action": fields.String,
    "c_id": fields.Integer, 
    "requester": fields.Integer, 
    "c_name": fields.String,
    "c_image": fields.String,
    "req_date": fields.String,  
    "status": fields.Integer,
    "last_update_date": fields.String,
    "comments": fields.String
}

class RequestConfirmation(Resource):

    @roles_accepted('store_manager','admin')
    @auth_required('token')
    def get(self):
        if current_user.roles[0].name=='admin':
            request_data = RequestOnCategory.query.filter_by(status=-1)\
                                            .order_by(RequestOnCategory.req_date.desc()).all()
            print(request_data)
        else:
            request_data = RequestOnCategory.query.filter_by(requester=current_user.id).all()
        if request_data==[]:
            return {'message': 'No Request made yet'}, 200
        return marshal(request_data, request_fields), 200
    
    @roles_required('store_manager') 
    @auth_required('token')
    def post(self):
        try:
            formData = request.form.to_dict()
            # print(formData)
            if (formData['action'] in ['POST','PUT']) and (not formData['c_name'].isalnum()):
                return {'message':'Category name must be of only one word'}, 202
            d = datetime.now()
            img_path = None
            if 'c_image' in request.files:
                image = request.files['c_image']
                folder = app.config['UPLOAD_FOLDER']+'pendingUpload/'
                count = len(os.listdir(folder))
                if image.filename != "":
                    img_path = image.filename.split('.')[0]+'_'+str(count)+'.'+image.filename.split('.')[-1]
                    # print(img_path)
                    image.save(os.path.join(folder,img_path))  
                    r1 = RequestOnCategory(**formData, c_image=img_path, requester=current_user.id,
                                            req_date=d)
            if img_path is None:
                r1 = RequestOnCategory(**formData, requester=current_user.id, req_date=d)
            db.session.add(r1)
            db.session.commit()
            return 200
        except ValueError as ve:
            return {'message':str(ve)}, 202
        except Exception as e:
            if ('UNIQUE constraint failed' in str(e.args[0])):
                print('UNIQUE constraint error ignored!')
                return
            else:
                print(e)
                return {'message': 'Creation Failed! Some Error Occured.'}, 500
    
class ReturnConfirmation(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('status', type=int, choices=[-1,1], help='Invalid Status')
        self.parser.add_argument('comment', type=str)

    @roles_required('admin')
    @auth_required('token')
    def put(self, cn_id):
        args = self.parser.parse_args()
        ap1 = RequestOnCategory.query.get(cn_id)
        ap1.comment = args['comment']
        ap1.status = args['status']
        ap1.last_update_date = datetime.now()
        db.session.commit()
        return 200

