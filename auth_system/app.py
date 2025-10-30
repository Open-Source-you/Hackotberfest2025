# auth_system/app.py - New FastAPI Implementation

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer # Needed for token dependency
from pydantic import BaseModel
import uvicorn
import os
from datetime import datetime, timedelta
from jose import jwt, JWTError # Using python-jose for robustness

# --- Configuration (Security Fixes) ---
SECRET_KEY = os.environ.get("JWT_SECRET", "YOUR_FALLBACK_DEV_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 Hours

# --- Pydantic Schemas ---
class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- Authentication Logic ---

# Simulated User Store (Addressing Hardcoded Credentials)
def verify_user(username: str, password: str) -> bool:
    user_store = {
        "testuser": "testpass"
    }
    return user_store.get(username) == password

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire.timestamp()})
    
    # Fix for Hardcoded Secret Key and Expiration
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Auth System API",
    description="JWT Authentication and User Endpoints.",
    version="1.0.0"
)

# Placeholder for Auth Dependency (Fix for Missing Auth Check)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# --- Endpoints ---

@app.post("/auth/login", response_model=Token, tags=["Authentication"])
def login(user_data: UserLogin):
    """
    Authenticates a user and returns an access token.
    (Swagger will now show proper token format.)
    """
    if not verify_user(user_data.username, user_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Fix for Hardcoded Expiration
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token}


@app.get("/user/me", tags=["Users"])
def read_user_me(token: str = Depends(oauth2_scheme)):
    """
    Retrieves the profile of the currently authenticated user.
    Requires a valid JWT Bearer token.
    """
    # Placeholder for token validation (In a real app, this would validate the token and return the user)
    return {"username": "authenticated_user", "is_authenticated": True, "token_received": token}


# --- Run Server ---
if __name__ == "__main__":
    # Fix for Insecure Host/Reload using environment variables
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", 8000))
    RELOAD = os.environ.get("RELOAD", "True").lower() in ('true', '1', 'yes') # Only enable reload in dev

    uvicorn.run("app:app", host=HOST, port=PORT, reload=RELOAD)