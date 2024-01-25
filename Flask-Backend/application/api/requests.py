import os
from datetime import datetime
from ..data.models.requests import *
from flask_restful import Resource, fields, marshal, reqparse
from ..data.database import db
from ..data.models.inventory import Category
from flask import current_app as app
from flask import request
from flask_login import login_required, current_user
from flask_security import auth_required, roles_required, roles_accepted

def validateRequest(form):
    if 'c_name' in form.keys():
        if not(form['c_name'].isalnum()):
            print('in1')
            return False
    return True

request_fields = {
    "cn_id": fields.Integer,
    "action": fields.String,
    "c_id": fields.Integer, 
    "requester": fields.Integer, 
    "c_name": fields.String,
    "c_image": fields.String,
    "req_date": fields.String,  
    "status": fields.Integer
}

class RequestConfirmation(Resource):

    @roles_accepted('store_manager','admin')
    @auth_required('token')
    def get(self):
        if current_user.roles[0].name=='admin':
            request_data = RequestOnCategory.query.filter_by(status=-1)\
                                            .order_by(RequestOnCategory.req_date.desc()).all()
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
            print(formData)
            if not validateRequest(formData):
                return {'message':'Category name must be one word'}, 202
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
                # print('image path None')
                r1 = RequestOnCategory(**formData, requester=current_user.id, req_date=d)
            db.session.add(r1)
            db.session.commit()
            return 200
        except ValueError as ve:
            return {'message':str(ve)}, 202
    
class ReturnConfirmation(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('status', type=int, choices=[0,1], help='Invalid Status')

    @roles_required('admin')
    @auth_required('token')
    def put(self, cn_id):
        args = self.parser.parse_args()
        r1 = RequestOnCategory.query.get(cn_id)
        print(Category.query.filter_by(c_name=r1.c_name).first(), r1.c_name)
        if args['status']==1:
            if r1.action == 'DELETE':
                c1 = Category.query.get(r1.c_id)
                if c1.product_count>0:
                    return {'message':'Category has active products, Please deny request!'}, 202
            elif r1.action == 'PUT' and not Category.query.get(r1.c_id):
                return {'message':'Category has been deleted, Please deny request!'}, 202
            elif r1.action=="POST" and (Category.query.filter_by(c_name=r1.c_name).first() is not None):
                print('in post')
                return {'message':'Category already exists, Please deny request!'}, 202
        r1.status = args['status']
        db.session.commit()
        if args['status']==1:
            return {'message':'Approved Request ID:'+str(r1.cn_id)}, 200
        else:
            return {'message':'Denied Request ID:'+str(r1.cn_id)}, 200

