from .database import db
 
## Admin class
class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True) #use for login
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20))
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Admin:{self.admin_id} {self.first_name} {self.last_name}'

## Customer class
class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20))
    mobile_number = db.Column(db.String(10), nullable=False) #use for login
    address = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Customer:{self.customer_id} {self.first_name} {self.last_name}'