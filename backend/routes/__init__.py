"""
Flask Blueprints Registry.
"""
from .auth_routes import auth_bp
from .profile_routes import profile_bp
from .prediction_routes import prediction_bp
from .history_routes import history_bp
from .dashboard_routes import dashboard_bp
from .model_routes import model_bp
from .health_routes import health_bp

def register_blueprints(app):
    """Registers all REST API blueprints with the Flask app."""
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(profile_bp, url_prefix="/api/profile")
    app.register_blueprint(prediction_bp, url_prefix="/api")
    app.register_blueprint(history_bp, url_prefix="/api/history")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(model_bp, url_prefix="/api/model")
    app.register_blueprint(health_bp, url_prefix="/api")
