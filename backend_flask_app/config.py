"""Flask configuration file"""
from os import environ, path
from dotenv import load_dotenv
basedir = path.abspath(path.dirname(__file__))
# load environment variables file
load_dotenv(path.join(basedir, '.env'))



class Config:
    """Base config"""
    SECRET_KEY = environ.get('SECRET_KEY') or 'HackMePleaseLol'
    #SQLALCHEMY_TRACK_MODIFICATIONS = False
    #QUESTIONS_PER_PAGE = 10
    #FILE_UPLOADS = "./uploads"
    # Define directories for saving images
    UPLOAD_FOLDER = 'flaskr/static/uploads/'
    OUTPUT_FOLDER = 'flaskr/static/outputs/'
    JWT_SECRET_KEY = "my_secret_key"
    # Set up MongoDB connection from the environment variable
    #MONGO_URI = 'mongodb+srv://'+environ.get("MONGO_USER")+':'+environ.get("MONGO_PASSWORD")+'@cluster0.bhizxqh.mongodb.net/flask-app'




class ProdConfig(Config):
    """ production config"""
    ENV = 'production'
    DEBUG = False
    TESTING = False
    #SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI')
    #FILE_UPLOADS = "./uploads"

class DevConfig(Config):
    """development config"""
    ENV = 'development'
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')
    #SQLALCHEMY_DATABASE_URI = environ.get('YUUPEE_DATABASE_URI')
    #FILE_UPLOADS = "./scv_file"

class TestConfig(DevConfig):
    """testing config"""
    TESTING = True
    #SQLALCHEMY_DATABASE_URI = environ.get('TEST_DATABASE_URI')
    #FILE_UPLOADS = "./scv_file"