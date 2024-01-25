from .database import db 
from .models.users import *
from .models.shopping import Transaction
from .models.offers import Offers, CustomerOffers
from ..utils import check_password, hash_password
from ..sec import datastore

def create_first():
    # create roles
    datastore.find_or_create_role(id=1, name='admin', description='Add Store Manager & CRUD on Categories Only.')
    datastore.find_or_create_role(id=2, name='store_manager', description='CRUD on Products Only.')
    datastore.find_or_create_role(id=3, name='customer', description='Read inventory data & CRUD on MyCart')
    db.session.commit()  
    if not datastore.find_user(email='nibedita.6302@gmail.com'):
        #creating the only admin
        admin1 = datastore.create_user(email='nibedita.6302@gmail.com', password=hash_password('admin.12'))
        datastore.add_role_to_user(admin1, 'admin')
    db.session.commit()    

class SetID:
    count = 1

    def set_count(self):
        t = Transaction.query.order_by(Transaction.t_id.desc()).first()
        if t is not None:
            SetID.count = t.t_id

    def next_id(self):
        print(SetID.count)
        SetID.count+=1
        return SetID.count
    
def new_customer_offer():
    if Offers.query.filter_by(o_name='Welcome Harvest').first() is None:
        offer = Offers(o_name='Welcome Harvest', description="New Customer Welcome Offer.",
                    discount=25, use_count=5, price=0)
        db.session.add(offer)
        db.session.commit() 
    