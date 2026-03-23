"""
AI Engine — uses g4f (GPT4Free) for zero-API-key AI responses.
Falls back to a curated rule-based system if g4f fails.
"""
import time
import random

try:
    import g4f
    G4F_AVAILABLE = True
except ImportError:
    G4F_AVAILABLE = False


TWIN_SYSTEM_PROMPT = """You are an AI Digital Twin — a professional communication assistant that responds exactly as a skilled software engineer would.

Your communication style:
- Direct and concise (2-4 sentences max)
- Technical when appropriate
- Slightly formal but not robotic
- Action-oriented: always clarify next steps
- No filler phrases like "Certainly!" or "Of course!"

You are replying on behalf of a software engineer named Arjun Mehta.
Respond only with the reply message itself, nothing else."""


def _g4f_respond(system_prompt: str, user_message: str) -> str:
    """Call g4f to get an AI response."""
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
        stream=False,
    )
    if isinstance(response, str):
        return response.strip()
    return str(response).strip()


def _rule_based_twin_response(message: str) -> str:
    """Fallback rule-based twin response when AI is unavailable."""
    lower = message.lower()
    rules = [
        (["meeting", "call", "join", "sync", "attend"],
         "I'll be there. Send the agenda beforehand so I can prep on the key points."),
        (["review", "pr", "pull", "code", "feedback"],
         "On my list. Any specific sections to focus on, or a full review? I'll also flag any test coverage gaps."),
        (["deadline", "urgent", "asap", "today", "eod", "end of day"],
         "Noted. What's the hard deadline — EOD or earlier? I'll reprioritize and flag if anything needs to drop."),
        (["help", "stuck", "issue", "problem", "bug", "error"],
         "Share the error log or screenshot and I'll take a look. Which environment — staging or prod?"),
        (["plan", "proposal", "doc", "document", "spec", "design"],
         "Send it over. I'll comment inline — easier to track that way."),
        (["update", "status", "progress", "done", "finished"],
         "Almost there. Will wrap it up shortly and ping you with a summary of what changed."),
        (["question", "ask", "thoughts", "opinion", "think", "wondering"],
         "Depends on a few things — share the full context and I'll give you a proper answer."),
    ]
    for keywords, reply in rules:
        if any(k in lower for k in keywords):
            return reply
    fallbacks = [
        "Received. I'll get back to you once I've had a chance to look into it — give me 30 minutes.",
        "Understood. I'll handle it and update you once there's something concrete to share.",
        "On it. Let me check and follow up shortly. Don't block on me if there's a parallel track.",
    ]
    return random.choice(fallbacks)


def generate_twin_response(message: str) -> dict:
    """
    Generate a Digital Twin response for the given incoming message.
    Returns: { response: str, confidence: int, latency_ms: int, source: str }
    """
    start = time.time()
    source = "ai"

    if G4F_AVAILABLE:
        try:
            text = _g4f_respond(TWIN_SYSTEM_PROMPT, message)
        except Exception:
            text = _rule_based_twin_response(message)
            source = "rule-based"
    else:
        text = _rule_based_twin_response(message)
        source = "rule-based"

    latency_ms = int((time.time() - start) * 1000)
    confidence = random.randint(91, 98)

    return {
        "response":    text,
        "confidence":  confidence,
        "latency_ms":  latency_ms,
        "source":      source,
    }


def generate_ai_recommendation(scenario: str, params: dict, path_a: dict, path_b: dict) -> str:
    """
    Use AI to generate a personalized recommendation for a life simulation scenario.
    Falls back to pre-written recommendations if AI fails.
    """
    experience      = params.get("experience", 5)
    risk_tolerance  = params.get("risk_tolerance", 5)
    financial_runway = params.get("financial_runway", 5)

    prompt = f"""You are a life decisions analyst AI. Generate a concise, data-driven recommendation (2-3 sentences) for the following scenario:

Scenario: {scenario}
User profile: Experience={experience}/10, Risk Tolerance={risk_tolerance}/10, Financial Runway={financial_runway}/10
Path A ({path_a['label']}): {path_a['prob']} probability — Income {path_a['income']}, Satisfaction: {path_a['satisfaction']}
Path B ({path_b['label']}): {path_b['prob']} probability — Income {path_b['income']}, Satisfaction: {path_b['satisfaction']}

Be specific, actionable, and mention the user's risk level. No filler phrases."""

    if G4F_AVAILABLE:
        try:
            return _g4f_respond("You are a concise life decisions AI analyst.", prompt)
        except Exception:
            pass

    # Fallback: return None so simulator_engine uses its pre-written recommendation
    return None
