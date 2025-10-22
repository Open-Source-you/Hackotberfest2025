Pull Request Overview

Adds a secure Flask-based authentication service with email/password, Google OAuth2, and JWT. Includes pinned installation requirements and clear documentation.

Key Changes
- Flask app with endpoints: POST /register, POST /login, GET /profile (JWT), GET /login/google, GET /login/google/callback
- JWT-based session management with 24-hour expiration
- Google OAuth2 login/callback flow
- Pinned dependencies for Flask, SQLAlchemy, OAuth, JWT, and requests
- README with setup and endpoint documentation

Security and Reliability Improvements
- Require SECRET_KEY via environment variable (no hardcoded fallback)
- Store passwords using werkzeug password hashing; verify using check_password_hash
- Validate input for required fields and types (email, password)
- Handle JWT errors explicitly (expired/invalid) and user-not-found cases
- Restrict CORS to trusted origins for auth endpoints
- Instantiate OAuth WebApplicationClient per request (thread-safe)
- Add robust error handling for Google discovery, token exchange, and userinfo requests
- Use SQLAlchemy 2.x-compatible db.session.get for lookups
- Control Flask debug mode via FLASK_DEBUG env var

Reviewed Changes
- auth_system/requirements.txt — required libraries to run Flask app with OAuth and JWT (removed deprecated Flask-OAuthlib)
- auth_system/app.py — authentication API, JWT issuance/validation, Google OAuth2 flow, and security hardening
- auth_system/README.md — setup steps, environment variables, and endpoint docs (added SECRET_KEY guidance)

Testing Notes
- Local testing with SQLite; JWT verified via Authorization: Bearer <token>
- Google OAuth requires setting GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET and valid redirect URI

Follow-ups
- Expand CORS allowed origins for staging/production frontends
- Add unit tests for endpoints and JWT middleware
- Consider refresh tokens or short-lived access tokens with refresh endpoint