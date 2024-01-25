from ..utils import *
from flask_restful import Resource
from flask_restful import fields, marshal
from flask_restful import reqparse
from ..data.database import db
from flask_login import  login_required, current_user

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
    'c_id' : fields.Integer #needed??
}

class Search(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('string', type=str.lower)
    
    def post(self):
        args = self.parser.parse_args()
        product_data = []
        product_data.extend(search_category(args['string']))
        product_data.extend(search_brand(args['string']))
        product_data.extend(search_product(args['string']))
        product_data = list(set(product_data))
        return marshal(product_data, product_fields), 200

