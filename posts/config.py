import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
load_dotenv()

class Config(object):
    DEBUG = False
    TESTING = False
    DB_NAME = os.getenv('MYSQL_DB')
    DB_USER = os.getenv('MYSQL_USER')
    DB_PASS = os.getenv('MYSQL_PASSWORD')
    DB_SERVICE = os.getenv('DB_SERVICE')
    DB_PORT = os.getenv('DB_PORT')
    SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@{2}:{3}/{4}'.format(
        DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME
    )

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'Secret_password!'
    db.init_app(app)

    return app