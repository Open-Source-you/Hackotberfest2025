# Auth System

A robust user authentication system for Hacktoberfest2025 using Flask, OAuth2 (Google), and JWT.

## Features
- User registration and login
- OAuth2 login (Google)
- JWT-based session management
- User profile endpoint

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set environment variables:
   - `SECRET_KEY` (required, use a strong random value)
   - `GOOGLE_CLIENT_ID` (for Google OAuth2)
   - `GOOGLE_CLIENT_SECRET` (for Google OAuth2)
3. Run the app:
   ```bash
   python app.py
   ```

## Endpoints
- `POST /register` — Register with email/password
- `POST /login` — Login with email/password
- `GET /profile` — Get user profile (JWT required)
- `GET /login/google` — OAuth2 login (Google)
- `GET /login/google/callback` — OAuth2 callback

## Notes
- Uses SQLite for demo purposes
- Ready for future integration with dashboards, notifications, etc.
