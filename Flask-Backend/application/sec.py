
from flask_security import SQLAlchemySessionUserDatastore
from .data.models.users import Users, Role
from .data.database import db

# Setup Flask-Security
datastore = SQLAlchemySessionUserDatastore(db.session, Users, Role)

