from datetime import datetime
from application.data.models.confirmation import *
from application.data.models.users import Users
from application.data.models.users import Logs
from flask_restful import Resource, fields, marshal, reqparse
from application.data.database import db
from flask import abort
from flask_login import login_required, current_user
from flask_security import auth_required, roles_required, roles_accepted

request_fields = {
    "cn_id": fields.Integer,
    "action": fields.String,
    "table_name": fields.String,
    "item_id": fields.Integer, 
    "requester": fields.Integer, 
    "update": fields.String, 
    "req_date": fields.String,  
    "url": fields.String, 
    "status": fields.Integer,
    "last_update_date": fields.String,
    "comments": fields.String
}

class RequestConfirmation(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('action', type=str, choices=['POST','PUT','DELETE'], help='Invalid Action')
        self.parser.add_argument('update', type=str)
        self.parser.add_argument('url', type=str)

    @roles_accepted('store_manager','admin')
    @login_required
    def get(self):
        if current_user.roles[0].name=='admin':
            request_data = Confirmation.query.filter_by(status=0)\
                                            .order_by(Confirmation.req_date.desc()).all()
            print(request_data)
        else:
            request_data = Confirmation.query.filter_by(requester=current_user.id).all()
        if request_data==[]:
            return {'message': 'No Request yet'}, 200
        return marshal(request_data, request_fields), 200
    
    @roles_required('store_manager')
    @login_required
    def post(self, table, id=-1):
        args = self.parser.parse_args()
        d = datetime.now()
        ap1 = Confirmation(**args, requester=current_user.id, table_name=table, item_id=id, req_date=d)
        db.session.add(ap1)
        db.session.commit()
        return 200
    
class ReturnConfirmation(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('status', type=int, choices=[-1,1], help='Invalid Status')
        self.parser.add_argument('comment', type=str)

    @roles_required('admin')
    @login_required
    def post(self, cn_id):
        args = self.parser.parse_args()
        ap1 = Confirmation.query.get(cn_id)
        ap1.comment = args['comment']
        ap1.status = args['status']
        ap1.last_update_date = datetime.now()
        db.session.commit()
        return 200

