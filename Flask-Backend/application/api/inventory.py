import os
from datetime import datetime
from ..data.models.inventory import *
from ..data.models.users import Users
from ..data.models.users import Logs
from ..utils import parseProductFromData
from flask_restful import Resource, fields, marshal, reqparse
from ..data.database import db
from ..redis_cache import cache
from flask import abort, request
from flask import current_app as app
from flask_login import login_required, current_user
from flask_security import auth_required, roles_required, roles_accepted

product_fields = {
    'p_id': fields.Integer,
    'p_name': fields.String,
    'p_description' : fields.String,
    'brand': fields.String,
    'p_qty' : fields.Integer,
    'unit': fields.String,
    'price' : fields.Float,
    'stock' : fields.Integer,
    'stock_remaining' : fields.Integer,
    'p_image': fields.String,
    'is_deleted': fields.Float,
    'expieryDate' : fields.String,
    'c_id' : fields.Integer,
    'creator': fields.Integer
}

class ProductCRUD(Resource):
    table_name = Products.__tablename__  
    
    def __init__(self):      
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('p_name', type=str)
        self.parser.add_argument('p_description', type=str)
        self.parser.add_argument('brand', type=str)
        self.parser.add_argument('p_qty', type=int)
        self.parser.add_argument('unit', type=str)
        self.parser.add_argument('price', type=float)
        self.parser.add_argument('stock', type=int)
        self.parser.add_argument('p_image', type=str)
        self.parser.add_argument('expieryDate', type=str)
        self.parser.add_argument('c_id', type=int)
     
    @cache.cached()
    def get(self, p_id):
        product_data = Products.query.get(p_id)
        return marshal(product_data, product_fields),  200
  
    @roles_required('store_manager')
    @auth_required('token')
    def post(self):
        id=1
        image = None
        try:
            formData = request.form.to_dict()
            formData = parseProductFromData(formData) # validating form
            print(formData)
            if Products.query.filter_by(**formData).first():
                raise Exception('UNIQUE constraint failed - Duplicate POST')
            """             
            if not formData['p_name'].isalnum():
                return {'message':'Product name must be of one word'}, 202 
            """
            p = Products.query.order_by(Products.p_id.desc()).first()
            p1 = Products(**formData, stock_remaining=formData['stock'], creator=current_user.id)
            if 'p_image' in request.files:
                image = request.files['p_image']
                if image.filename != "":
                    extension = '.'+image.filename.split('.')[-1]
                    if p is not None: #check if this one is the first category
                        id=p.p_id+1
                    img_path = formData['p_name'].split()[0].lower()+'_'+str(id)+extension
                    print(img_path)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER']+'upload/',img_path))
                    p1.p_image = img_path
            # increment category product_count
            c1 = Category.query.get(p1.c_id)
            c1.product_count+=1
            db.session.add(p1)
            # logs
            log = Logs(user_id=current_user.id, action='POST', table_name=self.table_name, 
                    action_on=id, date=datetime.now())
            db.session.add(log)
            db.session.commit()
            return {'message':'New Product Created'}, 200
        except Exception as e:
            if ('UNIQUE constraint failed' in str(e.args[0])):
                print('UNIQUE constraint error ignored!')
                return
            else:
                print(e)
                return {'message': 'Creation Failed! Some Error Occured.'}, 500 

    @roles_required('store_manager')
    @auth_required('token')
    def put(self, p_id):
        p1 = Products.query.get(p_id)
        if (p1.creator!=current_user.id):
            return {'message':'Permission Denied!'}, 403
        
        formData = request.form.to_dict()
        print(formData)
        formData = parseProductFromData(formData) # validating form
        print(formData)
        if 'p_name' in formData and (not formData['p_name'].isalnum()):
            return {'message':'Category name must be of only one word'}, 202
        for col in Products.__table__.columns:
            if col.name in formData:
                if col.name == 'stock':
                    p1.stock_remaining = formData['stock']
                setattr(p1,col.name,formData[col.name])
        if 'p_image' in request.files:
            image = request.files['p_image']
            if image.filename != "":
                old_image = os.path.join(app.config['UPLOAD_FOLDER']+'upload/',p1.p_image)
                extension = '.'+image.filename.split('.')[-1]
                img_path = formData['p_name'].lower()+'_'+str(p1.p_id)+extension
                image.save(os.path.join(app.config['UPLOAD_FOLDER']+'upload/',img_path))
                p1.p_image = img_path
                if os.path.exists(old_image):
                    os.remove(old_image)
        #logs
        log = Logs(user_id=current_user.id, action='PUT', table_name=self.table_name,
                action_on=p1.p_id, date=datetime.now(), is_admin=True)
        db.session.add(log)
        db.session.commit()
        return 200
    
    @roles_required('store_manager')
    @auth_required('token')
    def delete(self, p_id):
        p1 = Products.query.get(p_id)
        c1 = Category.query.get(p1.c_id)
        if (p1.creator!=current_user.id):
            return {'message':'Permission Denied!'}, 403
        p1.is_deleted = True
        c1.product_count-=1
        log = Logs(user_id=current_user.id, action='DELETE', table_name=self.table_name,
                   action_on=p_id, date=datetime.now(), is_admin=True)
        db.session.add(log)
        db.session.commit()
        return {'message':f'Product (p_id:{p_id}) deletion confirmed.'}, 200

class ProductCategoryView(Resource): #all products under a category
    @cache.cached()
    def get(self, c_id):
        product_data = Products.query.filter_by(c_id=c_id, is_deleted=0).all()
        return marshal(product_data, product_fields),  200
  
category_fields = {
    'c_id': fields.Integer,
    'c_name': fields.String,
    'product_count': fields.Integer,
    'c_image': fields.String,
    'o_id': fields.Integer
}

class CategoryGet(Resource): # get data of a category - incase of forms
    def get(self, c_id):
        category_data = Category.query.get(c_id)
        return marshal(category_data,category_fields),  200

class CategoryCRUD(Resource):
    table_name = Category.__tablename__ 

    def __init__(self):        
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('c_name', type=str)
        self.parser.add_argument('product_count', type=int)
        self.parser.add_argument('o_id', type=int)
        self.parser.add_argument('c_image', type=str)
    
    @cache.cached()
    def get(self):
        category_data = Category.query.all()
        return marshal(category_data,category_fields),  200
    
    @roles_required('admin')
    @auth_required('token')
    def post(self):
        id=1
        image = None
        try:
            formData = request.form.to_dict()
            print(formData)
            if not formData['c_name'].isalnum():
                return {'message':'Category name must be of only one word'}, 202 
            c = Category.query.order_by(Category.c_id.desc()).first()
            if c is not None and c.c_name == formData['c_name']:
                return {'message':'Category already exists'}, 202
            elif Category.query.filter_by(c_name=formData['c_name']).first() is not None:
                return {'message':'Category already exists'}, 202
            c1 = Category(**formData)
            if 'c_image' in request.files:
                image = request.files['c_image']
                if image.filename != "":
                    extension = '.'+image.filename.split('.')[-1]
                    if c is not None: #check if this one is the first category
                        id=c.c_id+1
                    img_path = formData['c_name'].lower()+'_'+str(id)+extension
                    print(img_path)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER']+'upload/',img_path))
                    c1.c_image = img_path
            db.session.add(c1)
            log = Logs(user_id=current_user.id, action='POST', table_name=self.table_name,
                    action_on=id, date=datetime.now(), is_admin=True)
            db.session.add(log)
            db.session.commit()
            return {'message':'New Category Created'}, 200
        except Exception as e:
            if ('UNIQUE constraint failed' in str(e.args[0])):
                print('UNIQUE constraint error ignored!')
                return 
            else:
                print(e)
                return {'message': 'Creation Failed! Some Error Occured.'}, 500

    @roles_required('admin')
    @auth_required('token')
    def put(self, c_id):
        image = None
        c1 = Category.query.get(c_id)
        try:
            formData = request.form.to_dict()
            # print(formData)
            if formData['c_name']!='' :
                if not formData['c_name'].isalnum(): #only 1 word for image nameing
                    # print('in - message1')
                    return {'message':'Category name must be of only one word'}, 202
                c1.c_name = formData['c_name']
            if 'c_image' in request.files:
                image = request.files['c_image']
                if image.filename != "":
                    old_image = os.path.join(app.config['UPLOAD_FOLDER']+'upload/',c1.c_image)
                    extension = '.'+image.filename.split('.')[-1]
                    img_path = formData['c_name'].lower()+'_'+str(c1.c_id)+extension
                    image.save(os.path.join(app.config['UPLOAD_FOLDER']+'upload/',img_path))
                    c1.c_image = img_path
                    if os.path.exists(old_image) and formData['c_name']!='':
                        print('in')
                        os.remove(old_image)
        except Exception as err:
            print('Error',err)
            return {'message': 'Creation Failed! Some Error Occured.'}, 500
        print(current_user, 'from login - authentication', current_user.is_authenticated)
        log = Logs(user_id=current_user.id, action='PUT', table_name=self.table_name,
                   action_on=c_id, date=datetime.now(), is_admin=True)
        db.session.add(log)
        db.session.commit()
        return 200
    
    @roles_required('admin')
    @auth_required('token')
    def delete(self, c_id): 
        c1 = Category.query.get(c_id)
        # print(c1.products)
        for p in c1.products:
            if not p.is_deleted:
                return {'message': f'Category has active products, CANNOT be deleted!'}
        db.session.delete(c1)
        log = Logs(user_id=current_user.id, action='DELETE', table_name=self.table_name,
                   action_on=c_id, date=datetime.now(), is_admin=True)
        db.session.add(log)
        db.session.commit()
        return {'message':f'Category (c_id:{c_id}) deletion confirmed.'}, 200
    
review_fields = {
    'email': fields.String,
    'review':fields.String,
    'rating': fields.Integer
}

class ReviewCRUD(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('review', type=str)
        self.parser.add_argument('rating', type=int)
    
    @cache.cached()
    def get(self, p_id):
        review_data = db.session.query(Review.review, Review.rating, Users.email)\
                                .join(Review, Review.user_id==Users.id).filter_by(p_id=p_id).all()
        return marshal(review_data, review_fields), 200
    
    @roles_required('customer')
    @auth_required('token')
    def post(self, p_id):
        try:
            args = self.parser.parse_args()
            r1 = Review(**args, user_id=current_user.id, p_id=p_id)
            db.session.add(r1)
            db.session.commit()
            return 200
        except Exception as e:
            if ('UNIQUE constraint failed' in str(e.args[0])):
                print('UNIQUE constraint error ignored!')
                return
            else:
                return Exception(e)
    
