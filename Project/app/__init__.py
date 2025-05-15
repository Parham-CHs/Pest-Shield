from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

from flask_mail import Mail , Message

# debug
import logging


# Initialize extensions without app context
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration

    # Enable detailed logging
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

    # db.init_app(app)    # Initialize the database
    # Migrate(app, db)  # Enable migrations  

    # with app.app_context():
    #     from app import routes  # Import routes
    #     db.create_all()  # Ensure tables exist

    db.init_app(app)
    mail.init_app(app)

    # Test mail configuration during startup
    with app.app_context():
        try:
            test_msg = Message("App Startup Test", 
                             recipients=["PestShieldGTA@gmail.com"])
            test_msg.body = "Flask mail configuration test(web app)"
            mail.send(test_msg)
            app.logger.info("✅ Startup test email sent successfully")
        except Exception as e:
            app.logger.error(f"❌ Mail configuration error: {str(e)}")


    # Ensure models are imported before creating tables
    from app import models

    with app.app_context():
        db.create_all()  # Creates tables if they don't exist

    # Register routes (no direct import)
    from app.routes import init_routes
    init_routes(app)

    return app