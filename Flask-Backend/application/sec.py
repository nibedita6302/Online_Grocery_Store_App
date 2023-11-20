
from flask_security import SQLAlchemySessionUserDatastore
from application.data.models.users import Users, Role
from application.data.database import db

# Setup Flask-Security
datastore = SQLAlchemySessionUserDatastore(db.session, Users, Role)

