import os
from flask import Flask, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
from oauthlib.oauth2 import WebApplicationClient
import requests

app = Flask(__name__)
# Restrict CORS to trusted origins and only for auth endpoints
allowed_origins = [
    "https://your-frontend.com",  # Replace with your actual frontend origin(s)
    # Add more trusted origins as needed
]
CORS(app, resources={
    r"/login": {"origins": allowed_origins, "supports_credentials": True},
    r"/register": {"origins": allowed_origins, "supports_credentials": True},
    r"/profile": {"origins": allowed_origins, "supports_credentials": True},
    r"/login/google": {"origins": allowed_origins, "supports_credentials": True},
    r"/login/google/callback": {"origins": allowed_origins, "supports_credentials": True},
}, supports_credentials=True)
secret_key = os.environ.get('SECRET_KEY')
if not secret_key:
    raise RuntimeError("SECRET_KEY environment variable must be set and not empty.")
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# OAuth2 config (Google example)
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise RuntimeError("Missing required OAuth credentials: GOOGLE_CLIENT_ID and/or GOOGLE_CLIENT_SECRET environment variables must be set.")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
# Do NOT instantiate WebApplicationClient as a module-level singleton.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))  # For local auth only
    oauth_provider = db.Column(db.String(50))
    oauth_id = db.Column(db.String(120))

# Helper: create JWT token
def create_jwt(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    if not isinstance(data['email'], str) or not isinstance(data['password'], str):
        return jsonify({'error': 'Invalid field types'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    password_hash = generate_password_hash(data['password'])
    user = User(email=data['email'], name=data.get('name'), password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    token = create_jwt(user)
    return jsonify({'token': token, 'user': {'email': user.email, 'name': user.name}})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    if not isinstance(data['email'], str) or not isinstance(data['password'], str):
        return jsonify({'error': 'Invalid field types'}), 400
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.password_hash or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = create_jwt(user)
    return jsonify({'token': token, 'user': {'email': user.email, 'name': user.name}})

@app.route('/profile', methods=['GET'])
def profile():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user = db.session.get(User, payload['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'email': user.email, 'name': user.name})
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

# OAuth2 login (Google example)
@app.route('/login/google')
def login_google():
    from oauthlib.oauth2 import WebApplicationClient
    client = WebApplicationClient(GOOGLE_CLIENT_ID)
    try:
        response = requests.get(GOOGLE_DISCOVERY_URL)
        response.raise_for_status()
        google_provider_cfg = response.json()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to fetch Google provider configuration', 'details': str(e)}), 503
    except ValueError as e:
        return jsonify({'error': 'Invalid response from Google provider', 'details': str(e)}), 502
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route('/login/google/callback')
def callback_google():
    from oauthlib.oauth2 import WebApplicationClient
    client = WebApplicationClient(GOOGLE_CLIENT_ID)
    code = request.args.get("code")
    try:
        response = requests.get(GOOGLE_DISCOVERY_URL)
        response.raise_for_status()
        google_provider_cfg = response.json()
        token_endpoint = google_provider_cfg["token_endpoint"]
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
        )
        token_response.raise_for_status()
        client.parse_request_body_response(token_response.text)
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        userinfo_response.raise_for_status()
        userinfo = userinfo_response.json()
        email = userinfo["email"]
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email, name=userinfo.get("name"), oauth_provider="google", oauth_id=userinfo["sub"])
            db.session.add(user)
            db.session.commit()
        token = create_jwt(user)
        return jsonify({'token': token, 'user': {'email': user.email, 'name': user.name}})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Network error during Google OAuth', 'details': str(e)}), 503
    except ValueError as e:
        return jsonify({'error': 'Invalid response from Google provider', 'details': str(e)}), 502
    except KeyError as e:
        return jsonify({'error': f'Missing expected key in Google response: {str(e)}'}), 502

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    app.run(debug=debug_mode)
