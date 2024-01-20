from ..database import db 

'''
This is inventory.py file from MODELS. This include Category, Products
and Review models. The Category model defines sections for products to be 
assigned. Lastly, the Review model is the customer review on a product.

===============================================================================
Relationships:
- Category and Products have many-to-many relationship.
- Products and Review have one-to-many relationship.
'''

class Category(db.Model):
    __tablename__ = 'category'
    c_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    c_name = db.Column(db.String, unique=True, nullable=False)
    product_count = db.Column(db.Integer, default=0, nullable=False)
    c_image = db.Column(db.String, unique=True, nullable=False)
    #category discount - applied on all products under category
    o_id = db.Column(db.Integer, db.ForeignKey('category_offers.o_id'))
    products = db.relationship('Products', backref='categories', cascade='all, delete, delete-orphan')

class Products(db.Model):
    __tablename__ = 'products'
    p_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    p_name = db.Column(db.String, nullable=False)
    p_description = db.Column(db.String)
    p_qty = db.Column(db.Float, nullable=False)
    brand = db.Column(db.String, nullable=False)
    unit = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    stock_remaining = db.Column(db.Integer, nullable=False)
    p_image = db.Column(db.String, unique=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    expieryDate = db.Column(db.Date, nullable=False)
    c_id = db.Column(db.Integer, db.ForeignKey('category.c_id')) #category
    creator = db.Column(db.Integer, db.ForeignKey('users.id')) # user - created by
    reviews = db.relationship('Review', lazy=True, cascade='all, delete, delete-orphan')

class Review(db.Model):
    __tablename__='review'
    r_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    p_id = db.Column(db.Integer, db.ForeignKey('products.p_id')) #products
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) #customer
    review = db.Column(db.String(400))
    rating = db.Column(db.Integer)
    __table_args__=(
        db.CheckConstraint('rating IN (1,2,3,4,5)', name='product_rating'),
    )

