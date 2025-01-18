from flask import Blueprint

# Import individual route files for each user type
from .auth import auth_bp
from .admin import admin_bp
from .professional import professional_bp
from .customer import customer_bp


# Initialize a blueprint for the main routes
main_bp = Blueprint('main', __name__)

# Register each blueprint with the main application
def init_app(app):
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(professional_bp, url_prefix='/professional')
    app.register_blueprint(customer_bp, url_prefix='/customer')
