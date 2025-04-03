from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration

    # db.init_app(app)    # Initialize the database
    # Migrate(app, db)  # Enable migrations  

    # with app.app_context():
    #     from app import routes  # Import routes
    #     db.create_all()  # Ensure tables exist

    db.init_app(app)

    # Ensure models are imported before creating tables
    from app import models

    with app.app_context():
        db.create_all()  # Creates tables if they don't exist

    # Register routes (no direct import)
    from app.routes import init_routes
    init_routes(app)

    return app
