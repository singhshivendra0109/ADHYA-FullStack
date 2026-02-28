from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

# 1. Hashing Configuration
# Using bcrypt to securely store passwords in tutor_db
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. JWT Security Settings
# IMPORTANT: These MUST match your oauth2.py file exactly
SECRET_KEY = "YOUR_SUPER_SECRET_KEY_FOR_SMVIT_PROJECT" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # 1 hour session for security

# --- PASSWORD UTILITIES ---

def hash_password(password: str):
    """
    Encodes plain text password into a secure bcrypt hash.
    Used during registration in users.py.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    """
    Checks if the login attempt matches the stored hash in the 'password' column.
    Used during login in auth.py.
    """
    return pwd_context.verify(plain_password, hashed_password)

# --- TOKEN UTILITIES ---

def create_access_token(data: dict):
    """
    Generates a JWT 'Digital ID' for the user session.
    Includes an expiration timestamp (exp) in the payload.
    """
    to_encode = data.copy()
    
    # Set expiration using UTC to avoid local server time conflicts
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Sign the token with your secret key
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt