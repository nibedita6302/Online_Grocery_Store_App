import os

basedir=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config():
	DEBUG=False
	SQLITE_DB_DIR=None
	SQLALCHEMY_DATABASE_URI=None
	SQLALCHEMY_TRACK_MODIFICATIONS=False 
	
class LocalDevelopmentConfig(Config):
	DEBUG=True
	UPLOAD_FOLDER=os.path.join(basedir,'static/images')
	SQLITE_DB_DIR=os.path.join(basedir,"db_directory")
	SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(SQLITE_DB_DIR
							,'grocery_shop_database_v2.sqlite3')
	PASSWORD=os.getenv('PASSWORD') #read password from terminal - environment
