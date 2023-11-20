'''from flask import current_app
from flask_restful import Api

api = current_app.Api()

from application.api.users import CustomerLogin
api.add_resource(CustomerLogin, "/customer/login")

from application.api.users import CustomerRegister
api.add_resource(CustomerRegister, "/customer/register")
'''