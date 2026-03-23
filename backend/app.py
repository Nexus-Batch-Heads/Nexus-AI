"""
NEXUS Backend — Flask Entry Point (with Auth)
"""
import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager

from routes.twin import twin_bp
from routes.simulator import simulator_bp
from routes.auth import auth_bp
from models import User, init_db
from config import FLASK_PORT, FLASK_DEBUG, SECRET_KEY

# Frontend files live one level up from backend/
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
app.secret_key = SECRET_KEY

CORS(app, origins=["*"], supports_credentials=True)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"error": "Authentication required.", "authenticated": False}), 401

# Register blueprints
app.register_blueprint(twin_bp,      url_prefix="/api")
app.register_blueprint(simulator_bp, url_prefix="/api")
app.register_blueprint(auth_bp,      url_prefix="/api")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "NEXUS Backend", "version": "1.0.0"})


# Serve login page
@app.route("/login")
def login_page():
    return send_from_directory(FRONTEND_DIR, "login.html")


# Serve the frontend for all other routes
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    full_path = os.path.join(FRONTEND_DIR, path)
    if path and os.path.exists(full_path):
        return send_from_directory(FRONTEND_DIR, path)
    return send_from_directory(FRONTEND_DIR, "index.html")


if __name__ == "__main__":
    try:
        init_db()
    except Exception as e:
        print(f"  [DB] Warning: Could not connect to MSSQL — {e}")
        print("  [DB] Check your MSSQL_CONNECTION_STRING in .env")
    print(f"\n  NEXUS is live at → http://localhost:{FLASK_PORT}\n")
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=FLASK_DEBUG)
