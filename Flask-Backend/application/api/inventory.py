import os
from datetime import datetime
from application.data.models.inventory import *
from application.data.models.users import Users
from application.data.models.users import Logs
from application.utils import parseProductFromData
from flask_restful import Resource, fields, marshal, reqparse
from application.data.database import db
from flask import abort, request
from flask import current_app as app
from flask_login import login_required, current_user
from flask_security import auth_required, roles_required, roles_accepted

product_fields = {
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
    'c_id' : fields.Integer #needed??
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
    
    def get(self, p_id):
        product_data = Products.query.get(p_id)
        return marshal(product_data, product_fields),  200
  
    @roles_required('store_manager')
    @login_required
    def post(self):
        id=1
        image = None
        try:
            formData = request.form.to_dict()
            formData = parseProductFromData(formData) # validating form
            print(formData)
            if not formData['p_name'].isalnum():
                return {'message':'Category name must be of only one word'}, 400
            p = Products.query.order_by(Products.p_id.desc()).first()
            p1 = Products(**formData, stock_remaining=formData['stock'])
            if 'p_image' in request.files:
                image = request.files['p_image']
                if image.filename != "":
                    extension = '.'+image.filename.split('.')[-1]
                    if p is not None: #check if this one is the first category
                        id=p.p_id+1
                    img_path = formData['p_name'].lower()+'_'+str(id)+extension
                    print(img_path)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'],img_path))
                    p1.p_image = img_path
            # increment category product_count
            c1 = Category.query.get(p1.c_id)
            c1.product_count+=1
            db.session.add(p1)
        except:
            return {'message': 'Creation Failed! Some Error Occured.'}, 500
        log = Logs(user_id=current_user.id, action='POST', table_name=self.table_name, 
                   action_on=id, date=datetime.now())
        db.session.add(log)
        db.session.commit()
        return {'message':'New Product Created'}, 200

    @roles_required('store_manager')
    @login_required
    def put(self, p_id):
        try:
            p1 = Products.query.get(p_id)
            formData = request.form.to_dict()
            formData = parseProductFromData(formData) # validating form
            if 'p_name' in formData and (not formData['p_name'].isalnum()):
                return {'message':'Category name must be of only one word'}, 400
            for col in Products.__table__.columns:
                if col.name in formData:
                    if col.name == 'stock':
                        p1.stock_remaining = formData['stock']
                    setattr(p1,col.name,formData[col.name])
            if 'p_image' in request.files:
                image = request.files['p_image']
                if image.filename != "":
                    old_image = os.path.join(app.config['UPLOAD_FOLDER'],p1.p_image)
                    extension = '.'+image.filename.split('.')[-1]
                    img_path = formData['p_name'].lower()+'_'+str(p1.p_id)+extension
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'],img_path))
                    p1.p_image = img_path
                    if os.path.exists(old_image):
                        os.remove(old_image)
        except Exception as e:
            print(e)
            return {'message': 'Creation Failed! Some Error Occured.'}, 500
        log = Logs(user_id=current_user.id, action='PUT', table_name=self.table_name,
                   action_on=p1.p_id, date=datetime.now(), is_admin=True)
        db.session.add(log)
        db.session.commit()
        return 200
    
    @roles_required('admin')
    @login_required
    def delete(self, p_id):
        p1 = Products.query.get(p_id)
        p1.is_deleted = True
        log = Logs(user_id=current_user.id, action='DELETE', table_name=self.table_name,
                   action_on=p_id, date=datetime.now(), is_admin=True)
        db.session.add(log)
        db.session.commit()
        return {'message':f'Product (p_id:{p_id}) deletion confirmed.'}, 200

class ProductCategoryView(Resource):
    def get(self, c_id):
        product_data = Products.query.filter_by(c_id=c_id).all()
        return marshal(product_data, product_fields),  200
  
category_fields = {
    'c_id': fields.Integer,
    'c_name': fields.String,
    'product_count': fields.Integer,
    'c_image': fields.String,
    'o_id': fields.Integer
}

class CategoryGet(Resource):
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
    
    def get(self):
        category_data = Category.query.all()
        return marshal(category_data,category_fields),  200
    
    @roles_required('admin')
    @login_required
    def post(self):
        id=1
        image = None
        try:
            formData = request.form.to_dict()
            print(formData)
            if not formData['c_name'].isalnum():
                return {'message':'Category name must be of only one word'}, 400
            c = Category.query.order_by(Category.c_id.desc()).first()
            c1 = Category(**formData)
            if 'c_image' in request.files:
                image = request.files['c_image']
                if image.filename != "":
                    extension = '.'+image.filename.split('.')[-1]
                    if c is not None: #check if this one is the first category
                        id=c.c_id+1
                    img_path = formData['c_name'].lower()+'_'+str(id)+extension
                    print(img_path)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'],img_path))
                    c1.c_image = img_path
            db.session.add(c1)
        except:
            return {'message': 'Creation Failed! Some Error Occured.'}, 500
        log = Logs(user_id=current_user.id, action='POST', table_name=self.table_name,
                   action_on=id, date=datetime.now(), is_admin=True)
        db.session.add(log)
        db.session.commit()
        return {'message':'New Category Created'}, 200

    @roles_required('admin')
    @login_required
    def put(self, c_id):
        image = None
        c1 = Category.query.get(c_id)
        try:
            formData = request.form.to_dict()
            c1.c_name = formData['c_name']
            if not formData['c_name'].isalnum():
                return {'message':'Category name must be of only one word'}, 400
            if 'c_image' in request.files:
                image = request.files['c_image']
                if image.filename != "":
                    old_image = os.path.join(app.config['UPLOAD_FOLDER'],c1.c_image)
                    extension = '.'+image.filename.split('.')[-1]
                    img_path = formData['c_name'].lower()+'_'+str(c1.c_id)+extension
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'],img_path))
                    c1.c_image = img_path
                    if os.path.exists(old_image):
                        os.remove(old_image)
        except:
            return {'message': 'Creation Failed! Some Error Occured.'}, 500
        log = Logs(user_id=current_user.id, action='PUT', table_name=self.table_name,
                   action_on=c_id, date=datetime.now(), is_admin=True)
        db.session.add(log)
        db.session.commit()
        return 200
    
    @roles_required('admin')
    @login_required
    def delete(self, c_id):
        c1 = Category.query.get(c_id)
        print(c1.products)
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
    
    def get(self, p_id):
        review_data = db.session.query(Review.review, Review.rating, Users.email)\
                                .join(Review, Review.user_id==Users.id).filter_by(p_id=p_id).all()
        return marshal(review_data, review_fields), 200
    
    @roles_required('customer')
    @login_required
    def post(self, p_id):
        args = self.parser.parse_args()
        r1 = Review(**args, user_id=current_user.id, p_id=p_id)
        db.session.add(r1)
        db.session.commit()
        return 200
    
