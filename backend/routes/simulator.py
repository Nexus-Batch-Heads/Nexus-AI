"""
Route: POST /api/simulate
Life Decision Simulator endpoint. Requires authentication.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required
from utils.simulator_engine import simulate, BASE_SCENARIOS
from utils.ai_engine import generate_ai_recommendation

simulator_bp = Blueprint("simulator", __name__)

VALID_SCENARIOS = list(BASE_SCENARIOS.keys())


@simulator_bp.route("/simulate", methods=["POST"])
@login_required
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

    # Clean up internal field
    result.pop("base_rec", None)

    return jsonify(result), 200
