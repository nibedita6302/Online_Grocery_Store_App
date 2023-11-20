from ..database import db 

class Confirmation(db.Model):
    __tablename__='confirmation'
    cn_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    action = db.Column(db.String, nullable=False) #POST/PUT/DELETE
    table_name = db.Column(db.String, nullable=False)
    item_id = db.Column(db.Integer, nullable=False) # product/category id
    requester = db.Column(db.Integer, db.ForeignKey('users.id'))
    update = db.Column(db.String) # json data 
    req_date = db.Column(db.DateTime, nullable=False)
    url = db.Column(db.String, nullable=False) #api url
    #filled by admin
    status = db.Column(db.Integer, default=0, nullable=False) 
    last_update_date = db.Column(db.DateTime)
    comments = db.Column(db.String) 
    __table_args__ = (
        # 1->Approved, 0->Denied, -1->Waiting
        db.CheckConstraint('status IN (-1,0,1)', name='status_validation'), 
        db.CheckConstraint("action IN ('POST','PUT','DELETE')", name='action_allowed')
    )


    # def set_update(self, dict_data):
    #     self.update = json.dumps(dict_data)
