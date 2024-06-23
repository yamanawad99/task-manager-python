from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from pymongo import MongoClient
from celery import Celery
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mongo_client = MongoClient(Config.MONGO_URI)
mongo_db = mongo_client.get_default_database()

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    celery.conf.update(app.config)

    from app import routes
    app.register_blueprint(routes.bp)

    return app