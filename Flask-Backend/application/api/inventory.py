from datetime import datetime
from application.data.models.inventory import *
from application.data.models.users import Users
from application.data.models.users import Logs
from flask_restful import Resource, fields, marshal, reqparse
from application.data.database import db
from flask import abort
from flask_login import login_required, current_user
from flask_security import auth_required, roles_required, roles_accepted

product_fields = {
    'p_name': fields.String,
    'p_description' : fields.String,
    'p_qty' : fields.Integer,
    'unit': fields.String,
    'price' : fields.Float,
    'stock' : fields.Integer,
    'stock_remaining' : fields.Integer,
    'p_image': fields.String,
    'is_deleted': fields.Float,
    'expieryDate' : fields.String,
    'c_id' : fields.Integer, #needed??
    'b_id' :fields.Integer
}

class ProductCRUD(Resource):
    table_name = Products.__tablename__  
    
    def __init__(self):      
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('p_name', type=str)
        self.parser.add_argument('p_description', type=str)
        self.parser.add_argument('p_qty', type=int)
        self.parser.add_argument('unit', type=str)
        self.parser.add_argument('price', type=float)
        self.parser.add_argument('stock', type=int)
        self.parser.add_argument('p_image', type=str)
        self.parser.add_argument('expieryDate', type=str)
        self.parser.add_argument('c_id', type=int)
        self.parser.add_argument('b_id', type=int)
    
    def get(self, p_id):
        product_data = Products.query.get(p_id)
        return marshal(product_data, product_fields),  200

    def get(self, c_id):
        product_data = Products.query.filter_by(c_id=c_id).all()
        return marshal(product_data, product_fields),  200
    
    @roles_required('store_manager')
    @login_required
    def post(self):
        try:
            args = self.parser.parse_args()
            args['expieryDate'] = datetime.strptime(args['expieryDate'],f'%Y-%m-%d')
            p1 = Products(**args, stock_remaining=args['stock'])
            c1 = Category.query.get(p1.c_id)
            c1.product_count+=1
            db.session.add(p1)
            db.session.commit()
        except:
            return {'message': 'Creation Failed! Some Error Occured.'}, 500
        p = Products.query.order_by(Products.p_id.desc()).first()
        log = Logs(user_id=current_user.id, action='POST', table_name=self.table_name, 
                   action_on=p.p_id, date=datetime.now())
        db.session.add(log)
        db.session.commit()
        return {'message':'New Product Created'}, 200

    @roles_required('store_manager')
    @login_required
    def put(self, p_id):
        args = self.parser.parse_args()
        p1 = Products.query.get(p_id)
        for col in Products.__table__.columns:
            if col.name in args:
                if col.name == 'expieryDate':
                    args['expieryDate'] = datetime.strptime(args['expieryDate'],f'%Y-%m-%d')
                setattr(p1,col.name,args[col.name])
        log = Logs(user_id=current_user.id, action='PUT', table_name=self.table_name,
                   action_on=p_id, date=datetime.now())
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

brand_fields = {
    'b_name' : fields.String,
    'b_description': fields.String
}

class BrandCRUD(Resource):
    table_name = Brands.__tablename__ 

    def __init__(self):    
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('b_name', type=str)
        self.parser.add_argument('b_description', type=str)
    
    def get(self, b_id):
        brand_data = Brands.query.get(b_id)
        print(brand_data)
        return marshal(brand_data,brand_fields),  200
    
    @roles_required('store_manager')
    @login_required
    def post(self):
        args = self.parser.parse_args()
        try:
            b1 = Brands(**args)
            db.session.add(b1)
            db.session.commit()
        except:
            return {'message': 'Creation Failed! Some Error Occured.'}, 500
        b = Brands.query.order_by(Brands.b_id.desc()).first()
        log = Logs(user_id=current_user.id, action='POST', table_name=self.table_name,
                   action_on=b.b_id, date=datetime.now())
        db.session.add(log)
        db.session.add(log)
        db.session.commit()
        return {'message':'New Brand Created'}, 200

    @roles_required('store_manager')
    @login_required
    def put(self, b_id):
        args = self.parser.parse_args()
        b1 = Brands.query.get(b_id)
        for col in Brands.__table__.columns:
            if col.name in args:
                setattr(b1,col.name,args[col.name])
        log = Logs(user_id=current_user.id, action='PUT', table_name=self.table_name,
                   action_on=b_id, date=datetime.now())
        db.session.add(log)
        db.session.commit()
        return 200
    
    @roles_required('store_manager')
    @login_required
    def delete(self, b_id):
        b1 = Brands.query.get(b_id)
        if b1.products != []:
            return {'message': f'Products under Brand (b_id:{b_id}) exists. CANNOT be deleted!'}
        db.session.delete(b1)
        log = Logs(user_id=current_user.id, action='DELETE', table_name=self.table_name,
                   action_on=b_id, date=datetime.now())
        db.session.add(log)
        db.session.commit()
        return {'message':f'Brand (b_id:{b_id}) deletion confirmed.'}, 200

category_fields = {
    'c_name': fields.String,
    'product_count': fields.Integer,
    'c_image': fields.String,
    'o_id': fields.Integer
}

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
        args = self.parser.parse_args()
        try:
            c1 = Category(**args)
            db.session.add(c1)
            db.session.commit()
        except:
            return {'message': 'Creation Failed! Some Error Occured.'}, 500
        c = Category.query.order_by(Category.c_id.desc()).first()
        log = Logs(user_id=current_user.id, action='POST', table_name=self.table_name,
                   action_on=c.c_id, date=datetime.now(), is_admin=True)
        db.session.add(log)
        db.session.commit()
        return {'message':'New Category Created'}, 200

    @roles_required('admin')
    @login_required
    def put(self, c_id):
        args = self.parser.parse_args()
        c1 = Category.query.get(c_id)
        c1.c_name = args['c_name']
        c1.c_image = args['c_image']
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
    
