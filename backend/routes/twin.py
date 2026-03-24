"""
Route: POST /api/twin/respond
Digital Twin chat response endpoint.
"""
import time
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from utils.ai_engine import generate_twin_response
from models_sqlite import Conversation

twin_bp = Blueprint("twin", __name__)


@twin_bp.route("/twin/respond", methods=["POST"])
def twin_respond():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "message field is required"}), 400

    if len(message) > 1000:
        return jsonify({"error": "message too long (max 1000 chars)"}), 400

    result = generate_twin_response(message)
    
    # Save to history if user is authenticated
    if current_user.is_authenticated:
        try:
            Conversation.save(
                user_id=current_user.id,
                message=message,
                response=result['response'],
                confidence=result['confidence'],
                latency_ms=result['latency_ms'],
                source=result['source']
            )
        except Exception as e:
            print(f"[WARN] Failed to save conversation: {e}")
    
    return jsonify(result), 200


@twin_bp.route("/twin/history", methods=["GET"])
@login_required
def twin_history():
    """Get conversation history for the current user."""
    limit = request.args.get('limit', 50, type=int)
    history = Conversation.get_history(current_user.id, limit)
    return jsonify({"history": history}), 200
