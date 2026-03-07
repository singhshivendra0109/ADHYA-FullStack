import os
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#  Hashing Configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# It looks for SECRET_KEY in Render/Vercel settings first.
# If not found, it uses your local string as a backup.
SECRET_KEY = os.getenv("SECRET_KEY", "YOUR_SUPER_SECRET_KEY_FOR_SMVIT_PROJECT") 
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Convert to int because env variables are always strings
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)) 


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


def create_access_token(data: dict):
    """
    Generates a JWT 'Digital ID' for the user session.
    Includes an expiration timestamp (exp) in the payload.
    """
    to_encode = data.copy()
    
    # Set expiration using UTC to avoid local server time conflicts
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Sign the token with the secret key retrieved from environment
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt