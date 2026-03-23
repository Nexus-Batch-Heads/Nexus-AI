"""
Route: POST /api/twin/respond
Digital Twin chat response endpoint. Requires authentication.
"""
import time
from flask import Blueprint, request, jsonify
from flask_login import login_required
from utils.ai_engine import generate_twin_response

twin_bp = Blueprint("twin", __name__)


@twin_bp.route("/twin/respond", methods=["POST"])
@login_required
def twin_respond():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "message field is required"}), 400

    if len(message) > 1000:
        return jsonify({"error": "message too long (max 1000 chars)"}), 400

    result = generate_twin_response(message)
    return jsonify(result), 200
