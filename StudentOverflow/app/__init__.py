from flask import Flask
from .supabase_client import supabase, get_user_from_session
from .auth import auth_bp
from .questions import q_bp
import os

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = os.getenv("elias_y_eluney", "dev-key-change-me")

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(q_bp)

    @app.context_processor
    def inject_user():
        return {"current_user": get_user_from_session()}

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app