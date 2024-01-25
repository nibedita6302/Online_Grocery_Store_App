from ..database import db 

'''
This is shopping.py file from MODELS. This includes models required to buy 
products. This include MyCart, Transaction models and ProductCart association
model. 
The MyCart model defines the cart_id for every customer. The Transaction model
stores the product and customer data for every succesful transactions. The
ProductCart model is an association table between Products and MyCart model. 
Every row in Transaction model is uniquely identified by t_id, p_id and cst_id.

===============================================================================
Relationships:
- MyCart and Customer have one-to-one relationship.
- MyCart and Products have many-to-many relationship.
- Transaction and Customer have many-to-many relationship.
- Transaction and Products have many-to-many relationship.
'''
 
class MyCart(db.Model):
    __tablename__ = 'my_cart'
    cart_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  #customer
    hasItems = db.relationship('Products', backref='addToCart', secondary = 'cart_product', cascade='all, delete')

# association table for MyCart and Products
class ProductCart(db.Model):
    __tablename__ = 'cart_product'
    cart_id = db.Column(db.Integer, db.ForeignKey('my_cart.cart_id'), primary_key=True)
    p_id = db.Column(db.Integer, db.ForeignKey('products.p_id'), primary_key=True) #products
    bought_qty = db.Column(db.Integer, nullable=False)

class Transaction(db.Model):
    __tablename__ = 'transaction'
    t_id = db.Column(db.Integer, primary_key=True) #create t_id with count
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) #mycart
    total_price = db.Column(db.Float, nullable=False)
    bought_date = db.Column(db.DateTime, nullable=False)

# association table for Transaction and Products
class TransactionProduct(db.Model):
    __tablename__='transaction_product'
    t_id = db.Column(db.Integer, db.ForeignKey('transaction.t_id'), primary_key=True)
    p_id = db.Column(db.Integer, db.ForeignKey('products.p_id'), primary_key=True)  
    bought_qty = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Float, nullable=False)
    # is_discount = db.Column(db.Boolean, nullable=False, default=False)
 