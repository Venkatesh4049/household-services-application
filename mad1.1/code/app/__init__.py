from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.professional import professional_bp
    from app.routes.customer import customer_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(professional_bp, url_prefix='/professional')
    app.register_blueprint(customer_bp, url_prefix='/customer')

    # Redirect root URL to login page
    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))

    with app.app_context():
        db.create_all()

    return app
