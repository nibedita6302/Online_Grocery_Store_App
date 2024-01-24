from datetime import datetime
from application.data.models.offers import *
from application.data.models.users import Logs, Users
from application.data.models.inventory import Category
from flask import request
from flask_restful import Resource
from flask_restful import fields, marshal
from flask_restful import reqparse
from application.data.database import db
from application.redis_cache import cache
from flask_login import  login_required, current_user
from flask_security import roles_required, auth_required

offer_fields = {
    'o_id': fields.Integer,
    'o_name': fields.String,
    'description': fields.String,
    'discount': fields.Integer,
    'use_count': fields.Integer,
    'price': fields.Float
}

class CustomerOfferCRUD(Resource):
    
    @cache.cached()
    def get(self):
        offer_data = Offers.query.filter_by(is_active=1).all()
        return marshal(offer_data, offer_fields), 200
    
    @roles_required('admin')
    @auth_required('token')
    def post(self):
        try:
            form = request.form.to_dict()
            offer = Offers(**form)
            db.session.add(offer)
            db.session.commit()
            # add to logs
            offer = Offers.query.order_by(Offers.o_id.desc()).first()
            log = Logs(user_id=current_user.id, action='POST', table_name=offer.__tablename__, 
                    action_on=offer.o_id, date=datetime.now())
            db.session.add(log)
            db.session.commit()
            return 200
        except Exception as e:
            if ('UNIQUE constraint failed' in str(e.args[0])):
                print('UNIQUE constraint error ignored!')
                return
            else:
                return Exception(e)
    
    @roles_required('customer')   # customer buying offer
    @auth_required('token')
    def put(self, o_id):
        is_co = CustomerOffers.query.filter_by(user_id=current_user.id).first()
        if is_co is None:
            cust_offer = CustomerOffers(user_id=current_user.id, o_id=o_id)
            cust_offer.set_use_count() 
            db.session.add(cust_offer)  
            db.session.commit()
            return {'message':'Payment of Successful! Offer added to account.'}, 200
        return {'message':'You can avail only one offer at a time'}, 202

    @roles_required('admin')
    @auth_required('token')
    def delete(self, o_id):
        # inactive the offer
        if o_id==1:
            return {'message':'Offer ID: 1 is a default offer, Cannot be deleted!'}, 202
        offer = Offers.query.get(o_id)
        offer.is_active=0
        # add to logs
        log = Logs(user_id=current_user.id, action='DELETE', table_name=offer.__tablename__, 
                   action_on=offer.o_id, date=datetime.now(), is_admin=1)
        db.session.add(log)
        db.session.commit()
        return {'message':f'Offer {o_id} has been deactivated'}, 200
    
"""
category_offer_fields = {
    'o_name': fields.String,
    'description': fields.String,
    'discount': fields.Integer
}

category_fields = {
    'c_id': fields.Integer
}


class CategoryOfferCRUD(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('o_name', type=str)
        self.parser.add_argument('description', type=str)
        self.parser.add_argument('discount', type=int)
    
    def get(self):
        category_offer_data = CategoryOffers.query.all()
        result = []
        for offer in category_offer_data:
            data = {
                'offer': marshal(category_offer_data, category_offer_fields),
                'category': marshal(offer.categories, category_fields)
            }
            result.append(data)
        return result, 200
    
    @roles_required('admin')
    @login_required
    def post(self, c_id):
        try:
            args = self.parser.parse_args()
            co = CategoryOffers(**args)
            db.session.add(co)
            db.session.commit()
            # add to logs
            offer = CategoryOffers.query.order_by(CategoryOffers.o_id.desc()).first()
            log = Logs(user_id=current_user.id, action='POST', table_name=offer.__tablename__, 
                    action_on=offer.o_id, date=datetime.now(), is_admin=1)
            catg = Category.query.get(c_id)
            catg.o_id = offer.o_id
            db.session.add(log)
            db.session.commit()
            return 200
        except Exception as e:
            if ('UNIQUE constraint failed' in str(e.args[0])):
                print('UNIQUE constraint error ignored!')
                return
            else:
                return Exception(e)        
    
    @roles_required('admin')
    @login_required
    def delete(self, o_id):
        co = CategoryOffers.query.get(o_id)
        db.session.delete(co)
        # add to logs
        log = Logs(user_id=current_user.id, action='DELETE', table_name=co.__tablename__, 
                   action_on=co.o_id, date=datetime.now(), is_admin=1)
        db.session.add(log)
        db.session.commit()
        return {'message':f'Offer {o_id} has been deleted'}, 200
"""