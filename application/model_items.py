from .database import db 


## Association of My Cart and Products Class
class CartProduct(db.Model): 
    __tablename__ = 'cart_product'
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('MyCart.cart_id'), primary_key=True)
    quantity_count = db.Column(db.Integer, nullable=False) 

    def __repr__(self):
        return f'<CartProduct:{self.cart_id} {self.product_id}>'

## Products Class 
class Products(db.Model):  
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
    product_name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    stock_count = db.Column(db.Integer, nullable=False)
    minAmount = db.Column(db.Integer, nullable=False)
    units = db.Column(db.String(10), nullable=False)
    seller = db.Column(db.String(20), nullable=False)
    totalSale_count = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.String(50))
    image_path = db.Column(db.String, unique=True)

    def __repr__(self):
        return f'<Products:{self.product_id} {self.product_name}>'

## Category Class
class Category(db.Model): 
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String(20), nullable=False)    
    product_count = db.Column(db.Integer, default=0)
    hasProducts = db.relationship('Products', backref='belongTo')

    def __repr__(self):  
        return f'<Category:{self.category_id} {self.category_name}>'

## My Cart Class
class MyCart(db.Model):
    __tablename__ = 'MyCart'
    cart_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    subtotal = db.Column(db.Numeric(10,2), nullable=False, default=0)
    hasItems = db.relationship('Products', backref='addToCart', secondary = 'cart_product')

    def __repr__(self):
        return f'<MyCart:{self.cart_id} {self.customer_id}>'

## Orders Class 
class Orders(db.Model): 
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    totalOrderAmount = db.Column(db.Numeric(10,2), nullable=False)
    bought_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Orders:{self.order_id}>' 
    
## Stores Transaction details of customers 
class Transaction(db.Model):
    __tablename__ = 'transactions'
    product_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), primary_key=True)
    product_name = db.Column(db.String(30), nullable=False)
    product_price = db.Column(db.Numeric(10,2), nullable=False)
    seller = db.Column(db.String(20), nullable=False)
    product_count = db.Column(db.Integer, nullable=False)
    totalProductAmount = db.Column(db.Numeric(10,2), nullable=False)
    
    def __repr__(self):
        return f'<Transactions:{self.order_id} {self.product_id}>'  