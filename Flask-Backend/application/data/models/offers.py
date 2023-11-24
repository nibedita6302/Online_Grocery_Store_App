from ..database import db 

'''
This is offers.py file from MODELS. This includes the model for creating an offer. This class
creates a general offer for any category or a particular user. Te possible offers
are "Discounts" and "Buy X get Y free".

User offer generally have unique time limit for each user, unlike categories. 
Thus, to solve this problem a custome class can be created that extends this class
and for every instance of the child class a seperate validity time can be set.
===================================================================================
Functions:
- Getter and Setter functions for _start_date, _validity and type.
- Apply function for discount and BGF (Buy and Get Free) set parameters for 
  respective offer and the _use_count for them. 
===================================================================================
Relationships:
- Offers and Category have one-to-many relationship.
- Offers and Customers have one-to-many relationship.
'''

class Offers(db.Model):
    __tablename__ = 'offers'
    o_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    o_name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    discount = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    use_count = db.Column(db.Integer) 
    price = db.Column(db.Float, nullable=False)

    def apply_discount(self, total_price):
        return total_price*self.discount/100
        
class CustomerOffers(db.Model):
    __tablename__ = 'customer_offers'
    o_id = db.Column(db.Integer, db.ForeignKey('offers.o_id'), primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    use_count = db.Column(db.Integer) # number of valid usage

    def set_use_count(self):
        offer = Offers.query.get(self.o_id)
        self.use_count=offer.use_count
    
class CategoryOffers(db.Model):
    __tablename__ = 'category_offers'
    o_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    o_name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    discount = db.Column(db.Integer)
    categories = db.relationship('Category', backref=db.backref('offers', lazy=True))
    
    def apply_discount(self, price):
        return price*self.discount/100
