import os
from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


app = None

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    if os.getenv('ENV', "development") == "production":
      app.logger.info("Currently no production config is setup.")
      raise Exception("Currently no production config is setup.")
    else:
      app.logger.info("Staring Local Development.")
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    app.logger.info("App setup complete")
    return app

app = create_app()
app.secret_key = b'd032_d9ur32-1/C2F56@fk03'


# Import all the controllers so they are loaded
from application.controller.admin_login import *
from application.controller.admin_control import *
from application.controller.admin_edit import *
from application.controller.customer_login import *
from application.controller.customer_all import *
from application.controller.customer_placeOrder import *
from application.controller.search import *

if __name__ == '__main__':
  # Run the Flask app
  print('Starting App')
  app.run(host='0.0.0.0',port=4100, debug=True)
