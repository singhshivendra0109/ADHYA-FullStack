
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from .database import engine
# from . import models
# from .routers import users, auth, profiles # Added profiles here
# from .routers import student_profile ,bookings,reviews,achievements,admin
# # 1. Create the tables in PostgreSQL
# models.Base.metadata.create_all(bind=engine)

# app = FastAPI(title="ADHYA: Backend Authentication Hub")

# # 2. CORS setup for your React ports
# # In main.py
# origins = [
#     "http://localhost:5173", 
#     "http://localhost:5174", 
#     "http://localhost:5175"  # Add this exact port
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # 3. Route Mounting
# app.include_router(auth.router, prefix="/api/auth")
# app.include_router(users.router, prefix="/api/users")
# app.include_router(profiles.router, prefix="/api/profiles") # Added the profile path
# app.include_router(student_profile.router)
# app.include_router(bookings.router)
# app.include_router(reviews.router)
# app.include_router(achievements.router)
# app.include_router(admin.router)

# @app.get("/")
# def root():
#     return {"status": "ADHYA API is Online"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import users, auth, profiles, student_profile, bookings, reviews, achievements, admin

# 1. Create the tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ADHYA: Backend Hub")

# 2. CORS setup
origins = [
    "http://localhost:5173", 
    "http://localhost:5174", 
    "http://localhost:5175"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Route Mounting - Standardizing prefixes to match React calls
# This makes Login available at /api/login and Signup at /api/users/
app.include_router(auth.router, prefix="/api/auth") 
app.include_router(users.router, prefix="/api/users")
app.include_router(profiles.router, prefix="/api/profiles")

# Mounting these with /api prefix as well for consistency
app.include_router(student_profile.router, prefix="/api/student")
app.include_router(bookings.router, prefix="/api/bookings")
app.include_router(reviews.router, prefix="/api/reviews")
app.include_router(achievements.router, prefix="/api/achievements")
app.include_router(admin.router, prefix="/api/admin")

@app.get("/")
def root():
    return {"status": "ADHYA API is Online"}