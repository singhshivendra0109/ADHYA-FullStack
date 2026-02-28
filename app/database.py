import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Password Security
# We use quote_plus to safely handle the '@' symbol in "Singh0109@"
raw_password = "Singh0109@"
safe_password = urllib.parse.quote_plus(raw_password)

# 2. Connection String
# Using 127.0.0.1 avoids common 'localhost' resolution issues on some systems
# Target database: tutor_db
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{safe_password}@127.0.0.1:5432/tutor_db"

# 3. Engine Configuration
# pool_pre_ping ensures the connection hasn't gone stale before use
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    echo=False # Set to True if you want to see the SQL queries in your terminal
)

# 4. Session Configuration
# We set autoflush=False to maintain manual control over database commits
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Model Base
# Every table (User, TutorProfile, StudentProfile) will inherit from this Base
Base = declarative_base()

# 6. Database Dependency
# This is used in your FastAPI routes to open and close DB connections automatically
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 7. Initializer Function
# Call this in your main.py to automatically generate tables if they don't exist
def init_db():
    # This will look at all models inheriting from 'Base' and create them in Postgres
    Base.metadata.create_all(bind=engine)