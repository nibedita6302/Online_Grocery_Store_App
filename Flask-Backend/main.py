import os
from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS
from application import config
from application.config import LocalDevelopmentConfig, StageConfig
from application.data.database import db
from flask_security import Security
from application.sec import datastore
from application.jobs import workers
#from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import LoginManager
from flask_security import utils
#from flask_sse import sse
from application.redis_cache import get_cache

# import logging
# logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = None
api = None
celery = None
cache = None

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="../Frontend", static_url_path='/static')
    print(os.getenv('ENV', "development"))
    if os.getenv('ENV', "development") == "production":
      app.logger.info("Currently no production config is setup.")
      raise Exception("Currently no production config is setup.")
    elif os.getenv('ENV', "development") == "stage":
      app.logger.info("Staring stage.")
      print("Staring  stage")
      app.config.from_object(StageConfig)
      print("pushed config")
    else:
      app.logger.info("Staring Local Development.")
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
      print("pushed config")
    
    app.app_context().push()
    print("DB Init")
    db.init_app(app)
    print("DB Init complete")
    
    #app.app_context().push()
    #app.logger.info("App setup complete")
    
    login_manager.init_app(app)

    # setting up flask security for Users
    app.security = Security(app, datastore)

    api = Api(app, prefix='/api')
    app.app_context().push()   
    CORS(app, supports_credentials=True)
    
    # Create celery   
    celery = workers.celery

    # Update with configuration
    celery.conf.update(
       broker_url = app.config["CELERY_BROKER_URL"],
       result_backend = app.config["CELERY_RESULT_BACKEND"]
    )
    celery.Task = workers.ContextTask
    app.app_context().push()
    print('Celery Initiated...')

    # setting up Cache
    cache = get_cache()
    cache.init_app(app)
    app.app_context().push()
    print('Cache Setup...')
    print("Create app complete")
    return app, api, celery

login_manager = LoginManager()

app ,api, celery= create_app()

# import models in main
from application.data.models.users import *
from application.data.models.offers import *
from application.data.models.shopping import *
from application.data.models.inventory import *
from application.data.models.requests import *
from application.data.default_data import create_first, new_customer_offer

with app.app_context():
  db.create_all()
  print('All models created.')
  create_first() #create default roles and admin
  new_customer_offer() #default new customer offer
  print('All default data created.')

@login_manager.user_loader
def load_user(user_id):
   return Users.query.get(int(user_id)) 

# Import all restful apis
# from application.api.users import api

from application.api.users import Login, Logout
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")

from application.api.users import CustomerRegister, StoreManagerRegister, AddressCRUD
api.add_resource(CustomerRegister, "/customer/register")
api.add_resource(StoreManagerRegister, '/store-manager/register')
api.add_resource(AddressCRUD, '/customer/<int:user_id>/address')

from application.api.users import ManagerApproval
api.add_resource(ManagerApproval,'/admin/store-manager-approvals','/admin/store-manager-approvals/<int:id>')

from application.api.inventory import ProductCRUD, ProductCategoryView, CategoryCRUD, CategoryGet, ReviewCRUD
api.add_resource(ProductCRUD, '/product/<int:p_id>', '/product/<int:p_id>/edit',
                  '/product/create', '/product/<int:p_id>/delete')
api.add_resource(ProductCategoryView, '/product/category/<int:c_id>',)
api.add_resource(CategoryCRUD, '/category', '/category/<int:c_id>/edit', '/category/create', 
                 '/category/<int:c_id>/delete')
api.add_resource(CategoryGet, '/category/<int:c_id>')
api.add_resource(ReviewCRUD, '/product/<int:p_id>/review', '/customer/product/<int:p_id>/review')

from application.api.requests import RequestConfirmation, ReturnConfirmation
api.add_resource(RequestConfirmation, '/requests', '/requests/create')
api.add_resource(ReturnConfirmation, '/admin/requests/<int:cn_id>')

from application.api.shopping import MyCartCRUD, TransactionConfirm, PlaceOrder
api.add_resource(MyCartCRUD, '/customer/<int:user_id>/mycart', '/customer/mycart/delete/<int:p_id>',
      '/customer/mycart/update/<int:p_id>', '/customer/<int:user_id>/add/product/<int:p_id>')
api.add_resource(TransactionConfirm, '/customer/<int:user_id>/transaction', 
                 '/customer/<int:user_id>/transaction/add')
api.add_resource(PlaceOrder, '/customer/<int:user_id>/place-order')

from application.api.offers import CustomerOfferCRUD
api.add_resource(CustomerOfferCRUD, '/offers-customer', '/offers-customer/<int:o_id>/delete',
                '/offers-customer/create', '/customer/buy-offer/<int:o_id>')
# api.add_resource(CategoryOfferCRUD, '/offers-category', '/offers-category/add/<int:c_id>', 
#                  '/offers-category/<int:o_id>/delete')

from application.api.search import Search
api.add_resource(Search, '/search')

from application.api.test import *

if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=8000, debug=True)