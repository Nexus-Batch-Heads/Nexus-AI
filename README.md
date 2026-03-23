# NEXUS-AI: Predictive Digital Twin and Decision Simulation Platform

## 1. System Overview
NEXUS-AI is a hybrid web platform that exposes an HTTP API for two tightly coupled inference domains:

1. Digital Twin response generation (language-model-assisted conversational emulation).
2. Multi-scenario decision simulation (structured deterministic/probabilistic path projection).

The platform is implemented as a Flask monolith with modular route registration and utility-layer execution engines. The frontend is a static SPA-like experience served directly by Flask, removing cross-origin deployment complexity in the default topology.

## 2. Runtime Topology and Request Flow
Execution model:

1. Flask app process boots from backend/app.py.
2. Configuration is loaded from environment variables via python-dotenv.
3. Blueprints are mounted under /api.
4. Frontend static assets are resolved from the repository root by Flask static routing.
5. API requests are dispatched to one of three domain route modules:
	 - backend/routes/twin.py
	 - backend/routes/simulator.py
	 - backend/routes/auth.py

Nominal request path:

1. Client issues HTTP request.
2. Flask URL map resolves blueprint endpoint.
3. Request payload is parsed with request.get_json(silent=True).
4. Input validation and normalization execute in route layer.
5. Route delegates computation to utility/model layer.
6. Result is serialized as JSON with explicit HTTP status semantics.

## 3. Backend Architecture Details
### 3.1 Core Service Layer
- Framework: Flask 3.x
- CORS policy: wildcard origin with credentials support enabled for compatibility with browser session cookies.
- Session/auth stack: Flask-Login user loader + unauthorized handler.
- Entry process host binding: 0.0.0.0 for container or LAN accessibility.

### 3.2 Route Surface
- GET /api/health
	- Liveness probe for service-level monitoring.
	- Returns service metadata and version marker.

- POST /api/twin/respond
	- Consumes message input.
	- Performs request-level constraints (required field, max length).
	- Invokes utility inference engine to produce response payload with confidence and latency metadata.

- POST /api/simulate
	- Consumes scenario key and param vector.
	- Clamps normalized integer parameters to bounded domain [1, 10].
	- Executes simulator engine for path A/B outcome generation.
	- Appends AI recommendation synthesis fallback over base deterministic recommendation.

- Auth endpoints under /api/auth/*
	- register, login, logout, me.
	- Uses bcrypt hash verification and Flask-Login session state.

### 3.3 Data and Identity Model
Persistence adapter uses pyodbc against Microsoft SQL Server.

users table logical schema:

1. id INT IDENTITY PRIMARY KEY
2. name NVARCHAR(120) NOT NULL
3. email NVARCHAR(255) UNIQUE NOT NULL
4. password_hash NVARCHAR(255) NOT NULL
5. created_at DATETIME defaulting to server clock

Authentication semantics:

1. User credential hash generation: bcrypt.gensalt + bcrypt.hashpw.
2. Password verification: bcrypt.checkpw.
3. Session identity hydration: Flask-Login user_loader maps user_id to persisted row.

## 4. Simulation Engine Characteristics
The simulator operates as a bounded-parameter outcome generator with scenario-specific base models. Each simulation emits:

1. scenario identifier and question framing.
2. normalized input params.
3. dual trajectory outputs (optimal vs risk path).
4. timeline events per trajectory.
5. quantitative/qualitative outcome fields (income and satisfaction classes).
6. recommendation and action tags.

The execution model is deterministic for base scenario structure and optionally stochastic/LLM-enhanced for recommendation language enrichment.

## 5. Digital Twin Inference Pipeline
Twin response generation is mediated through utility abstractions in backend/utils/ai_engine.py. The route contract expects generated payload fields including response text, source attribution, confidence estimation, and latency instrumentation. This enables UI-side telemetry display without additional tracing infrastructure.

## 6. Configuration and Environment Contract
Critical environment parameters:

1. FLASK_PORT
2. FLASK_DEBUG
3. SECRET_KEY
4. MSSQL_CONNECTION_STRING
5. GEMINI_API_KEY (or equivalent upstream model key, depending on configured provider path)

Default SQL Server transport assumes ODBC Driver 18 and can include TrustServerCertificate=yes for development environments with self-signed or non-public CA chains.

## 7. Infrastructure and Dependency Constraints
Python package dependencies include:

1. flask
2. flask-cors
3. flask-login
4. python-dotenv
5. bcrypt
6. pyodbc
7. g4f

Host-level requirement for MSSQL connectivity:

1. Microsoft ODBC driver installation (msodbcsql18 on Ubuntu).
2. Reachable SQL Server endpoint (local or remote).
3. Valid credential mode (Trusted_Connection or UID/PWD), aligned with runtime host OS and SQL Server auth policy.

## 8. Operational Notes
### 8.1 Health and Diagnostics
- /api/health confirms process readiness but not database readiness.
- DB connection failures in startup path are currently warning-tolerant; API routes touching persistence can still fail at runtime if DB is unavailable.

### 8.2 Security Considerations
- Current CORS wildcard settings are permissive and suitable only for development or tightly controlled deployments.
- Production hardening should restrict origin allowlist, rotate SECRET_KEY, and enforce TLS termination upstream.

### 8.3 Performance Considerations
- AI inference latency is external-provider-sensitive and non-deterministic.
- Route-level JSON parsing and validation overhead is negligible relative to model inference time.
- Synchronous Flask worker model implies request concurrency scaling is process/thread-count dependent; production WSGI tuning is recommended.

## 9. High-Precision Summary
NEXUS-AI is a Flask-based, API-first, dual-domain intelligence service that combines deterministic decision simulation and adaptive language response synthesis, with optional SQL-backed identity/session management and environment-driven runtime portability across local, containerized, and cloud-adjacent deployment targets.
