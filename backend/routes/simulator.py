"""
Route: POST /api/simulate
Life Decision Simulator endpoint.
"""
from flask import Blueprint, request, jsonify
from flask_login import current_user
from utils.simulator_engine import simulate, BASE_SCENARIOS
from utils.ai_engine import generate_ai_recommendation
from models_sqlite import Simulation

simulator_bp = Blueprint("simulator", __name__)

VALID_SCENARIOS = list(BASE_SCENARIOS.keys())


@simulator_bp.route("/simulate", methods=["POST"])
def run_simulation():
    data = request.get_json(silent=True) or {}

    scenario_key = (data.get("scenario") or "career").lower()
    if scenario_key not in VALID_SCENARIOS:
        return jsonify({
            "error": f"Invalid scenario. Must be one of: {', '.join(VALID_SCENARIOS)}"
        }), 400

    # Extract and clamp params to 1–10 range
    raw_params = data.get("params") or {}
    params = {
        "experience":       max(1, min(10, int(raw_params.get("experience",       5)))),
        "risk_tolerance":   max(1, min(10, int(raw_params.get("risk_tolerance",   5)))),
        "financial_runway": max(1, min(10, int(raw_params.get("financial_runway", 5)))),
    }

    result = simulate(scenario_key, params)
    if not result:
        return jsonify({"error": "Simulation failed"}), 500

    # Try to get an AI-enhanced recommendation
    ai_rec = generate_ai_recommendation(
        scenario_key, params, result["pathA"], result["pathB"]
    )
    result["recommendation"] = ai_rec if ai_rec else result["base_rec"]

    # Save to history if user is authenticated
    if current_user.is_authenticated:
        try:
            path_a_prob = int(result["pathA"]["prob"].split("%")[0])
            path_b_prob = int(result["pathB"]["prob"].split("%")[0])
            Simulation.save(
                user_id=current_user.id,
                scenario=scenario_key,
                params=params,
                path_a_prob=path_a_prob,
                path_b_prob=path_b_prob,
                recommendation=result["recommendation"]
            )
        except Exception as e:
            print(f"[WARN] Failed to save simulation: {e}")

    # Clean up internal field
    result.pop("base_rec", None)

    return jsonify(result), 200


@simulator_bp.route("/simulate/history", methods=["GET"])
def simulation_history():
    """Get simulation history for the current user."""
    if not current_user.is_authenticated:
        return jsonify({"error": "Authentication required"}), 401
    
    limit = request.args.get('limit', 20, type=int)
    history = Simulation.get_history(current_user.id, limit)
    return jsonify({"history": history}), 200
