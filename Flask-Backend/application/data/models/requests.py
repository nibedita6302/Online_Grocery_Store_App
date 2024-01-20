from ..database import db 
from ..models.inventory import Category 

class RequestOnCategory(db.Model):
    __tablename__='confirmation'
    cn_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    action = db.Column(db.String, nullable=False) #POST/PUT/DELETE
    c_id = db.Column(db.Integer, nullable=False) # for PUT and DELETE request
    # fill for POST and PUT requests
    c_name = db.Column(db.String, nullable=False)
    c_image = db.Column(db.String, nullable=False)
    # store-manager data
    requester = db.Column(db.Integer, db.ForeignKey('users.id'))
    req_date = db.Column(db.DateTime, nullable=False)
    #filled by admin
    status = db.Column(db.Integer, default=-1, nullable=False) 
    last_update_date = db.Column(db.DateTime)
    comments = db.Column(db.String) 
    # relationships
    # category = db.relationship('Category',back_populates='requests')
    
    __table_args__ = (
        # 1->Approved, 0->Denied, -1->Pending
        db.CheckConstraint('status IN (-1,0,1)', name='status_validation'), 
        db.CheckConstraint("action IN ('POST','PUT','DELETE')", name='action_allowed')
    )

    def isProperRequest(self):
        if self.action in ['PUT','DELETE']:
            if not Category.query.get(self.c_id):
                return False
        elif self.action in 'POST':
            if self.c_image == '' and self.c_name=='':
                return False
        elif self.c_name != '':
            if Category.query.filter_by(c_name=self.c_name):
                return False 
        return True
    
    def isDuplicateRequest(self):
        # not duplicate
        if self.c_id is not None:
            r1 = RequestOnCategory.query.filter_by(action=self.action, c_id=self.c_id, status=1).first() #accepted
            r_1 = RequestOnCategory.query.filter_by(action=self.action, c_id=self.c_id, status=-1).first() #pending
            return (r1 is None) and (r_1 is None) #not accepted or pending
        elif self.c_name!='' and self.c_image!='':
            r1 = RequestOnCategory.query.filter_by(action=self.action, c_name=self.c_name, #accepted
                                              c_image=self.c_image, status=1).first() 
            r_1 = RequestOnCategory.query.filter_by(action=self.action, c_name=self.c_name, #pending
                                              c_image=self.c_image, status=-1).first()
            return (r1 is None) and (r_1 is None) #not accepted or pending
        # duplicate
        return True
            
