import os
from flask import Flask, jsonify
from flask_login import LoginManager, UserMixin, current_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash

from .config import Config
from .models import db, Product

# For simplicity, admin user is hardcoded here.
# In a real app, you might want to store users in the database.
class AdminUser(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        if user_id == Config.ADMIN_USERNAME: # Using username as id for simplicity
            # In a real app, you'd query the database here.
            # For this hardcoded user, we need to ensure the password hash is available.
            # We'll generate it on app start if not already set (though this is not ideal for production)
            # A better approach for a single admin user is to pre-hash the password.
            hashed_password = generate_password_hash(Config.ADMIN_PASSWORD) # Hash it every time for get, or store it
            return AdminUser(Config.ADMIN_USERNAME, Config.ADMIN_USERNAME, hashed_password)
        return None

    @staticmethod
    def get_by_username(username):
        if username == Config.ADMIN_USERNAME:
            hashed_password = generate_password_hash(Config.ADMIN_PASSWORD)
            return AdminUser(Config.ADMIN_USERNAME, Config.ADMIN_USERNAME, hashed_password)
        return None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


login_manager = LoginManager()
login_manager.login_view = 'admin_login' # The route name for the login page
login_manager.login_message_category = 'info'
login_manager.login_message = "请登录以访问此页面。"


@login_manager.user_loader
def load_user(user_id):
    # For this simple setup, user_id is the username
    return AdminUser.get(user_id)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Initialize CSRF protection
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Ensure the upload folder exists
    if not os.path.exists(Config.UPLOAD_FOLDER):
        os.makedirs(Config.UPLOAD_FOLDER)

    # Import and register blueprints here later if we structure with blueprints
    # For now, routes will be in this file or imported directly.

    # Example: Register a simple health check route
    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy", "message": "Application is running."})

    # Command to create database tables
    @app.cli.command("create-db")
    def create_db_command():
        """Creates the database tables."""
        with app.app_context():
            db.create_all()
        print("Database tables created.")

    # Command to create a default admin (if you move users to DB)
    # @app.cli.command("create-admin")
    # def create_admin_command():
    #     """Creates the admin user."""
    #     # Add logic to create admin in DB
    #     print("Admin user created/updated.")


    # Import routes after app and db initialization to avoid circular imports
    from . import routes # We will create routes.py soon
    routes.register_routes(app) # Register the routes

    # Context processors
    @app.context_processor
    def inject_now():
        from datetime import datetime
        return {'now': datetime.utcnow()}

    return app

# This is useful if you run `python -m xianyu_manager.app` or similar
# However, for `flask run`, Flask detects `create_app` or `make_app` factory.
if __name__ == '__main__':
    app = create_app()
    app.run(debug=Config.DEBUG)
