from datetime import datetime
from application.data.default_data import SetID
from application.data.models.shopping import *
from application.data.models.offers import *
from application.data.models.inventory import Products, Category
from application.data.models.users import Users
from flask_restful import Resource
from flask_restful import fields, marshal
from flask_restful import reqparse
from application.data.database import db
from flask_login import  login_required
from flask_security import roles_required

mycart_fields = {
    'cart_id': fields.Integer
}

incart_product_fields = {
    'p_name': fields.String(attribute='Products.p_name'),
    'p_description' : fields.String(attribute='Products.p_description'),
    'p_qty' : fields.Integer(attribute='Products.p_qty'),
    'unit': fields.String(attribute='Products.unit'),
    'price' : fields.Float(attribute='Products.price'),
    'stock_remaining' : fields.Integer(attribute='Products.stock_remaining'),
    'bought_qty': fields.Integer(attribute='ProductCart.bought_qty'),
    'p_image': fields.String(attribute='Products.p_image')
}

class MyCartCRUD(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('bought_qty', type=int)

    @roles_required('customer')
    @login_required
    def get(self, user_id):
        mycart_data = MyCart.query.filter_by(user_id=user_id).first()
        products = mycart_data.hasItems
        incart_product_data = []
        for p in products:
            new_p = db.session.query(Products, ProductCart)\
                    .join(ProductCart, Products.p_id==ProductCart.p_id)\
                    .filter(ProductCart.cart_id==mycart_data.cart_id, Products.p_id==p.p_id).first()
            incart_product_data.append(new_p)
        result = {
            'mycart': marshal(mycart_data, mycart_fields),
            'products': marshal(incart_product_data, incart_product_fields)
        }
        return result, 200
    
    @roles_required('customer')
    @login_required
    def post(self, user_id, p_id):
        args = self.parser.parse_args()
        mycart = MyCart.query.filter_by(user_id=user_id).first()
        prodExist = ProductCart.query.filter_by(p_id=p_id, cart_id=mycart.cart_id).first()
        if prodExist:                       ## if product exist update
            prodExist.bought_qty += args['bought_qty']
        else:                               ## if product doesnot exist in cart - create
            cp = ProductCart(cart_id=mycart.cart_id, p_id=p_id,bought_qty=args['bought_qty'])
            db.session.add(cp)
        db.session.commit()
        return {'message':'Product added to Cart'}, 200
    
    @roles_required('customer')
    @login_required
    def put(self, user_id, p_id):
        args = self.parser.parse_args()
        mycart = MyCart.query.filter_by(user_id=user_id).first()
        product = ProductCart.query.filter_by(p_id=p_id, cart_id=mycart.cart_id).first()
        product.bought_qty = args['bought_qty']
        db.session.commit()
        return 200

    @roles_required('customer')
    @login_required
    def delete(self, user_id, p_id):
        mycart = MyCart.query.filter_by(user_id=user_id).first()
        product = ProductCart.query.filter_by(p_id=p_id, cart_id=mycart.cart_id).first()
        db.session.delete(product)
        db.session.commit()
        return {'message':'Product deleted from Cart'}, 200

transaction_fields = {
    'p_name': fields.String,
    'bought_qty': fields.Integer,
    'paid': fields.Float,
    'is_discount': fields.Boolean
}

class TransactionConfirm(Resource):
    @roles_required('customer')
    @login_required
    def get(self, user_id):
        trans = Transaction.query.filter_by(user_id=user_id).all()
        result = []
        for t in trans:
            transaction_data = db.session.query(TransactionProduct.bought_qty, TransactionProduct.paid,
                                TransactionProduct.is_discount, Products.p_name)\
                                .join(TransactionProduct, TransactionProduct.p_id==Products.p_id)\
                                .filter(TransactionProduct.t_id==t.t_id).all()
            print(transaction_data)
            data = {
                't_id': t.t_id,
                'total_price': t.total_price,
                'bought_date': t.bought_date.strftime(f'%Y-%m-%d'),
                'products': marshal(transaction_data, transaction_fields)
            }
            result.append(data)
        return result, 200
        
obj = SetID()
obj.set_count()

class PlaceOrder(Resource):    
    @roles_required('customer')
    @login_required
    def post(self, user_id):
        mycart = MyCart.query.filter_by(user_id=user_id).first()
        products = mycart.hasItems
        id = obj.next_id()
        if products==[]:
            return {'message':'Empty Cart!'}, 200
        total_price = 0
        for p in products:
            pc = ProductCart.query.filter_by(cart_id=mycart.cart_id, p_id=p.p_id).first()
            # applying category offer to products individually
            discount, is_discount =0, False
            offer = Category.query.get(p.c_id).offers
            if offer is not None:                 
                discount-=offer.apply_discount(p.price)
                is_discount=True
            total_price+=(p.price-discount)*pc.bought_qty
            # add product to transaction
            tp = TransactionProduct(t_id=id, p_id=p.p_id, bought_qty=pc.bought_qty,
                                     paid=(p.price-discount)*pc.bought_qty, is_discount=is_discount )
            p.stock_remaining-=pc.bought_qty
            db.session.add(tp)
            db.session.delete(pc) #delete product from mycart
        # apply offer on total price if any
        cust_offer = CustomerOffers.query.filter_by(user_id=user_id).first()
        if cust_offer is not None:
            offer = Offers.query.get(cust_offer.o_id)
            total_price-=offer.apply_discount(total_price)
            cust_offer.use_count-=1
        date = datetime.now()
        t = Transaction(t_id=id, total_price=total_price, user_id=user_id, bought_date=date)
        db.session.add(t)
        db.session.commit() 
        return {'message':'Order Placed!'}, 200

