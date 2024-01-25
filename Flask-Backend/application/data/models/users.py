from ..database import db 
from flask_security import UserMixin, RoleMixin
from ...utils import check_password

'''
This is users.py file from MODELS. This includes models for all users which includes
users, Store managers and Admins. Store managers and Admins both belong to the
table/class named users since, both fall under users/admin priviledges. 

Other classes involve Logs for users CRUD operations. As well as Address and
Feedback tables for users. In addition usershas relationship with offers.
The table my_cart is used to store usersid and cart id.

===============================================================================
Relationships:
- usersand Address have one-to-many relationship.
- usersand Feedback have one-to-many relationship.
- usersand my_cart have one-to-one relationship.
- usersand Offers have many-to-one relationship.
- users and Logs have one-to-many relationship.
'''

RoleUsers = db.Table('role_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id'), primary_key=True), #users
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id'), primary_key=True) #Role
    ) 

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(200))

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    #phone = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Integer, nullable=False, default=1) 
    fs_uniquifier = db.Column(db.String(255), unique=True) 
    #relationships
    roles = db.relationship('Role', secondary=RoleUsers, backref='assignedTo', cascade='all, delete')
    addresses = db.relationship('Address', lazy=True, cascade='all, delete')
    reviews = db.relationship('Review', cascade='all, delete')
    transactions = db.relationship('Transaction', lazy=True, cascade='all, delete')
    prodCreated = db.relationship('Products', backref='createdBy') # store-manager created products
    __table_args__= (
        # 0->Denied, -1->Waiting, 1->Approved
        db.CheckConstraint('active IN (-1,0,1)', name='user_active'),
    )
    def match_password(self, password):
        return  check_password(password, self.password)

class Address(db.Model):
    __tablename__ = 'address'
    a_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    address = db.Column(db.String, nullable=False)
    pincode = db.Column(db.String(7), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) #users

class Logs(db.Model):
    __tablename__ = 'logs'
    log_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  #users
    is_admin = db.Column(db.Boolean, default=0, nullable=False)
    action = db.Column(db.String(6), nullable=False) # CREATE, UPDATE, DELETE
    table_name = db.Column(db.String, nullable=False)
    action_on = db.Column(db.Integer, nullable=False) # id of product/category
    date = db.Column(db.DateTime, nullable=False)
    # relationships
    manager_log = db.relationship('Users', backref=db.backref('loggedBy'))



