"""
Auth routes: register, login, logout, me
"""
import time
from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data     = request.get_json(silent=True) or {}
    name     = (data.get("name")     or "").strip()
    email    = (data.get("email")    or "").strip().lower()
    password = (data.get("password") or "").strip()

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required."}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters."}), 400
    if "@" not in email:
        return jsonify({"error": "Invalid email address."}), 400

    user = User.create(name, email, password)
    if user is None:
        return jsonify({"error": "An account with this email already exists."}), 409

    login_user(user, remember=True)
    return jsonify({
        "message": "Account created successfully.",
        "user": {"id": user.id, "name": user.name, "email": user.email}
    }), 201


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data     = request.get_json(silent=True) or {}
    email    = (data.get("email")    or "").strip().lower()
    password = (data.get("password") or "").strip()

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    user = User.verify_password(email, password)
    if user is None:
        return jsonify({"error": "Invalid email or password."}), 401

    login_user(user, remember=True)
    return jsonify({
        "message": "Logged in successfully.",
        "user": {"id": user.id, "name": user.name, "email": user.email}
    }), 200


@auth_bp.route("/auth/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out."}), 200


@auth_bp.route("/auth/me", methods=["GET"])
def me():
    if current_user.is_authenticated:
        return jsonify({
            "authenticated": True,
            "user": {
                "id":    current_user.id,
                "name":  current_user.name,
                "email": current_user.email,
            }
        }), 200
    return jsonify({"authenticated": False}), 200
