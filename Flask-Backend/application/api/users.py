from application.data.models.users import *
from application.data.models.offers import CustomerOffers
from application.data.models.shopping import MyCart
from application.utils import hash_password
from flask_restful import Resource, Api, fields, marshal, reqparse
from application.data.database import db
from application.sec import datastore
from flask import abort
from flask_login import login_user, logout_user, login_required, current_user
from flask_security import auth_required, roles_required, auth_token_required

# api = Api(prefix="/api")

login_fields = {
	'id': fields.Integer,
    'message': fields.String,
    'role': fields.String,
    'token': fields.String
} 

class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type=str, help='Enter registered email id.', required=True)
        self.parser.add_argument('password', type=str, help='Enter valid password.', required=True)
    
    def post(self):
        args = self.parser.parse_args()
        u = Users.query.filter_by(email=args['email']).first()
        if u is not None:
            if u.active==0 and u.roles[0].name=='store_manager':
                return {'message':'Your Registration is not yet Approved.'}, 401
            elif u.active==-1 and u.roles[0].name=='store_manager':
                return {'message':'Your Registration has been denied.'}, 401
            if u.match_password(args['password']):
                login_user(u)
                # print(current_user, 'from login - authentication', current_user.is_authenticated)
                # print(current_user.get_auth_token(), current_user.get_auth_token()==current_user.fs_uniquifier)
                login_data = {'id':u.id,
                              'message':'Login Successful', 
                              'role':u.roles[0].name,
                              'token': current_user.get_auth_token()
                            }
                return marshal(login_data, login_fields), 200
            return {'message':'Invalid Password'}, 401
        return {'message':'Email not registered'}, 401
    
class Logout(Resource):
    def get(self):
        print(current_user, 'from logout - authentication', current_user.is_authenticated)
        logout_user()
        return {'message':'Logged Out!'}, 200

class CustomerRegister(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type=str, help='Enter valid email id.', required=True)
        #self.parser.add_argument('phone', type=str, help='Enter 10 digit phone number.', required=True)
        self.parser.add_argument('password', type=str, 
                help='Enter minimum 8 digit password with atleast 1 special character.', required=True)
    
    def post(self):
        args = self.parser.parse_args()
        if (Users.query.filter_by(email=args['email']).first() is None):
            c = datastore.create_user(email=args['email'], password=hash_password(args['password']))
            datastore.add_role_to_user(c, 'customer')
            db.session.add(c)
            db.session.commit()
            u1 = Users.query.filter_by(email=args['email']).first()
            mc = MyCart(user_id=u1.id)   # assign a cart to every new customer
            co = CustomerOffers(user_id=u1.id, o_id=1)
            print(co)
            co.set_use_count()
            db.session.add(mc)
            db.session.add(co)
            db.session.commit()
            return {'message':'Successfully registered new Users.', 'token':u1.fs_uniquifier}, 200
        return {'message': 'Email already exists.'}, 400

class StoreManagerRegister(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type=str, help='Enter valid email id.', required=True)
        self.parser.add_argument('password', type=str, 
                help='Enter minimum 8 digit password with atleast 1 special character.', required=True)
    
    def post(self):
        args = self.parser.parse_args()
        if (Users.query.filter_by(email=args['email']).first() is None):
            sm = datastore.create_user(email=args['email'], password=hash_password(args['password']), active=0)
            datastore.add_role_to_user(sm, 'store_manager')
            db.session.add(sm)
            db.session.commit()
            sm1 = Users.query.filter_by(email=args['email']).first()
            return {'message':'Registration Successful.', 'token':sm1.fs_uniquifier}, 200
        return {'message': 'Email already exists.'}, 400

store_manager_fields = {
    "id": fields.Integer,
    "email": fields.String
}

class ManagerApproval(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('approved', type=int, choices=[-1,1], help='Invalid Choice')
    
    @roles_required('admin')
    @auth_required('token')
    def get(self):
        data = Users.query.filter_by(active=0)
        store_manager_data = []
        for d in data:
            if d.roles[0].name=='store_manager':
                store_manager_data.append(d)
        return marshal(store_manager_data, store_manager_fields), 200
    
    @roles_required('admin')
    @auth_required('token')
    def post(self, id):
        args = self.parser.parse_args()
        sm = Users.query.get(id)
        sm.active = args['approved']
        db.session.commit()
        if args['approved']==1:
            return {'message': f'You approved {sm.email} as Store Manager'}, 200
        else:
            return {'message': f'You denied {sm.email} as Store Manager'}, 200
    
address_fields = { 
    'address': fields.String,
    'pincode': fields.String
} 

class AddressCRUD(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('a_id', type=int)
        self.parser.add_argument('address', type=str)
        self.parser.add_argument('pincode', type=str, help='Enter only 7 digits.')

    @roles_required('customer')
    @auth_required('token')
    def get(self, user_id):
        args = self.parser.parse_args()
        c = Users.query.get(user_id)
        return marshal(c.addresses, address_fields), 200
    
    @roles_required('customer')
    @auth_required('token')
    def post(self, user_id):
        args = self.parser.parse_args()
        a1 = Address(**args, user_id=user_id)
        db.session.add(a1)
        db.session.commit()
        return 200
    
    @roles_required('customer') 
    @auth_required('token')
    def put(self, user_id):
        args = self.parser.parse_args()
        a1 = Address.query.get(args['a_id'])
        a1.address = args['address']
        a1.pincode = args['pincode']
        db.session.commit()
        return 200
    
    @roles_required('customer')
    @auth_required('token')
    def delete(self, user_id):
        args = self.parser.parse_args()
        a1 = Address.query.get(args['a_id'])
        db.session.delete(a1)
        db.session.commit()
        return 200
    

# api.add_resource(Login, "/login")
# api.add_resource(Logout, "/logout")
# api.add_resource(CustomerRegister, "/customer/register")
# api.add_resource(StoreManagerRegister, '/store-manager/register')
# api.add_resource(AddressCRUD, '/customer/<int:user_id>/address')
# api.add_resource(ManagerApproval,'/admin/store-manager-approvals','/admin/store-manager-approvals/<int:id>')
