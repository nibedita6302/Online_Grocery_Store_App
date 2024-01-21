from ..database import db 
from ..models.inventory import Category 

class RequestOnCategory(db.Model):
    __tablename__='request_on_category'

    def __init__(self, action, requester, req_date, c_id=None, c_name='', c_image=''):
        if self.isProperRequest(action, c_id, c_name, c_image):
            if self.isDuplicateRequest(action, c_id, c_name, c_image):
                raise ValueError("Request already exists")
        else:
            raise ValueError("Invalid Request")
        
        self.action = action
        self.c_id = c_id
        self.c_name = c_name
        self.c_image = c_image
        self.requester = requester
        self.req_date = req_date

    cn_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    action = db.Column(db.String, nullable=False) #POST/PUT/DELETE
    c_id = db.Column(db.Integer) # for PUT and DELETE request
    # fill for POST and PUT requests
    c_name = db.Column(db.String)
    c_image = db.Column(db.String)
    # store-manager data
    requester = db.Column(db.Integer, db.ForeignKey('users.id'))
    req_date = db.Column(db.DateTime, nullable=False)
    #filled by admin
    status = db.Column(db.Integer, default=-1, nullable=False) 
    
    __table_args__ = (
        # 1->Approved, 0->Denied, -1->Pending
        db.CheckConstraint('status IN (-1,0,1)', name='status_validation'), 
        db.CheckConstraint("action IN ('POST','PUT','DELETE')", name='action_allowed')
    )

    def isProperRequest(self, action, c_id, c_name, c_image):
        if action in ['PUT','DELETE']:
            if not Category.query.get(c_id):
                # print('put-delete')
                return False
        elif action in 'POST':
            if c_image == '' and c_name=='' and c_id is None:
                # print('post')
                return False
        return True
    
    def isDuplicateRequest(self, action, c_id, c_name, c_image):
        # not duplicate
        if c_id is not None:
            r1 = RequestOnCategory.query.filter_by(action=action, c_id=c_id, status=1).first() #accepted
            r_1 = RequestOnCategory.query.filter_by(action=action, c_id=c_id, status=-1).first() #pending
            # print(r1,r_1)
            return (r1 is not None) and (r_1 is not None) #not accepted or pending
        elif c_name!='' and c_image!='':
            r1 = RequestOnCategory.query.filter_by(action=action, c_name=c_name, #accepted
                                              c_image=c_image, status=1).first() 
            r_1 = RequestOnCategory.query.filter_by(action=action, c_name=c_name, #pending
                                              c_image=c_image, status=-1).first()
            # print(r1,r_1,'next')
            return (r1 is not None) and (r_1 is not None) #not accepted or pending
        # duplicate
        return True
            
