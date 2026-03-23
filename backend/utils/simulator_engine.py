"""
Simulator Engine — probabilistic life decision simulation.
Adjusts base scenario probabilities using user-supplied slider parameters.
"""

BASE_SCENARIOS = {
    "career": {
        "question": "Switching from software engineering to product management at a mid-size startup.",
        "pathA": {
            "label": "Growth Trajectory",
            "base_prob": 62,
            "timeline": [
                {"time": "0–6 months",   "event": "Onboarding friction, salary dip of ~15%"},
                {"time": "6–18 months",  "event": "Product ownership, skill acceleration"},
                {"time": "18–36 months", "event": "Senior PM role, 40% comp recovery"},
            ],
            "income": "+28% in 3 years",
            "satisfaction": "High",
            "incomeClass": "positive",
            "satClass": "positive",
        },
        "pathB": {
            "label": "Friction Scenario",
            "base_prob": 38,
            "timeline": [
                {"time": "0–6 months",   "event": "Role mismatch, knowledge gaps surface"},
                {"time": "6–12 months",  "event": "Performance review pressure, burnout risk"},
                {"time": "12–18 months", "event": "Pivot back to engineering or restart search"},
            ],
            "income": "-12% over 18 months",
            "satisfaction": "Low–Medium",
            "incomeClass": "negative",
            "satClass": "negative",
        },
        "base_rec": "Based on your profile, transitioning is advisable if you complete a product management course within 3 months of starting. Building technical PM credibility first reduces your risk scenario probability significantly.",
        "tags": ["PM Certification", "Side Project Validation", "Network Building"],
    },
    "startup": {
        "question": "Leaving a stable corporate job to launch a SaaS product in the EdTech space.",
        "pathA": {
            "label": "Traction Path",
            "base_prob": 55,
            "timeline": [
                {"time": "0–3 months", "event": "MVP built, initial user testing complete"},
                {"time": "3–9 months", "event": "First 100 paying customers, product-market fit signals"},
                {"time": "9–24 months","event": "Seed funding secured, team expansion"},
            ],
            "income": "Variable, +200% potential upside",
            "satisfaction": "Very High",
            "incomeClass": "positive",
            "satClass": "positive",
        },
        "pathB": {
            "label": "Stall Scenario",
            "base_prob": 45,
            "timeline": [
                {"time": "0–6 months",  "event": "Product development delays, budget overrun"},
                {"time": "6–12 months", "event": "Low acquisition, churn above threshold"},
                {"time": "12–18 months","event": "Runway exhausted, return to employment"},
            ],
            "income": "-40% over 18 months",
            "satisfaction": "Low",
            "incomeClass": "negative",
            "satClass": "negative",
        },
        "base_rec": "Validate with a minimum of 20 paying customers before resigning. A side-launch approach for 3 months reduces failure probability while preserving income stability.",
        "tags": ["Customer Discovery", "Side Launch First", "Find Co-Founder"],
    },
    "relocation": {
        "question": "Relocating from Pune to Bangalore for a senior role at a Series B tech company.",
        "pathA": {
            "label": "Opportunity Path",
            "base_prob": 70,
            "timeline": [
                {"time": "0–3 months",   "event": "Settling-in costs, social friction period"},
                {"time": "3–12 months",  "event": "Accelerated career growth, new network built"},
                {"time": "12–30 months", "event": "Leadership visibility, 35–50% comp growth"},
            ],
            "income": "+38% in 2.5 years",
            "satisfaction": "High",
            "incomeClass": "positive",
            "satClass": "positive",
        },
        "pathB": {
            "label": "Isolation Risk",
            "base_prob": 30,
            "timeline": [
                {"time": "0–6 months",  "event": "Higher cost of living erodes net savings"},
                {"time": "6–12 months", "event": "Social isolation impacts performance"},
                {"time": "12–18 months","event": "Return relocation or role misalignment"},
            ],
            "income": "Neutral over 18 months",
            "satisfaction": "Medium",
            "incomeClass": "positive",
            "satClass": "negative",
        },
        "base_rec": "The move is strongly recommended given your career stage. Establish housing near a professional community hub and plan at least two in-person networking events per month in the first quarter.",
        "tags": ["Community Hub Living", "Early Networking", "Cost Buffer Planning"],
    },
    "investment": {
        "question": "Allocating 30% of liquid savings into a diversified equity + mutual fund portfolio over 5 years.",
        "pathA": {
            "label": "Growth Scenario",
            "base_prob": 68,
            "timeline": [
                {"time": "0–12 months", "event": "Portfolio establishment, 8–10% annualized returns"},
                {"time": "1–3 years",   "event": "Compounding effect, mid-cap exposure smooths volatility"},
                {"time": "3–5 years",   "event": "Target corpus reached, 2.1x capital growth"},
            ],
            "income": "+2.1x in 5 years",
            "satisfaction": "High",
            "incomeClass": "positive",
            "satClass": "positive",
        },
        "pathB": {
            "label": "Volatility Scenario",
            "base_prob": 32,
            "timeline": [
                {"time": "0–12 months", "event": "Market correction, -20% paper loss"},
                {"time": "1–2 years",   "event": "Panic exit triggers realized losses"},
                {"time": "2–5 years",   "event": "Missed recovery, 1.1x only vs 2.1x potential"},
            ],
            "income": "1.1x over 5 years",
            "satisfaction": "Low",
            "incomeClass": "negative",
            "satClass": "negative",
        },
        "base_rec": "SIP-based monthly allocation over lump sum reduces timing risk by 44%. Avoid reviewing portfolio more than once per month. Combined large-cap + index fund allocation outperforms pure active managed funds in this profile.",
        "tags": ["SIP Strategy", "Index Fund Allocation", "Annual Rebalancing"],
    },
}


def _adjust_probability(base_prob: int, experience: int, risk_tolerance: int, financial_runway: int) -> int:
    """
    Adjust the Path A probability based on user slider inputs (1–10 scale).
    Higher experience, risk tolerance, and financial runway → better odds.
    """
    # Normalize to -1..+1 range (5 is neutral midpoint)
    exp_delta      = (experience      - 5) * 1.2   # up to ±6%
    risk_delta     = (risk_tolerance  - 5) * 0.8   # up to ±4%
    runway_delta   = (financial_runway - 5) * 1.0  # up to ±5%

    adjusted = base_prob + exp_delta + risk_delta + runway_delta
    return max(20, min(85, round(adjusted)))  # clamp 20–85%


def simulate(scenario_key: str, params: dict) -> dict | None:
    """
    Run a life decision simulation for the given scenario and user params.
    Returns the full simulation result dict, or None if scenario not found.
    """
    scenario = BASE_SCENARIOS.get(scenario_key)
    if not scenario:
        return None

    experience       = params.get("experience",       5)
    risk_tolerance   = params.get("risk_tolerance",   5)
    financial_runway = params.get("financial_runway", 5)

    path_a_data = dict(scenario["pathA"])  # type: ignore[arg-type]
    path_b_data = dict(scenario["pathB"])  # type: ignore[arg-type]

    base_prob_a: int = int(path_a_data.get("base_prob", 60))  # type: ignore[arg-type]
    prob_a = _adjust_probability(base_prob_a, experience, risk_tolerance, financial_runway)
    prob_b = 100 - prob_a

    path_a = {**path_a_data, "prob": f"{prob_a}% probability"}
    path_b = {**path_b_data, "prob": f"{prob_b}% probability"}

    return {
        "scenario":   scenario_key,
        "question":   scenario["question"],
        "params": {
            "experience":       experience,
            "risk_tolerance":   risk_tolerance,
            "financial_runway": financial_runway,
        },
        "pathA":   path_a,
        "pathB":   path_b,
        "base_rec": scenario["base_rec"],
        "tags":    scenario["tags"],
    }
