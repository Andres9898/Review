from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.config import Config
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    from app.auth.routes import auth_bp
    from app.proveedores.routes import proveedores_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(proveedores_bp, url_prefix='/providers')

    return app