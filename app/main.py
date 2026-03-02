
# # # from fastapi import FastAPI
# # # from fastapi.middleware.cors import CORSMiddleware
# # # from .database import engine
# # # from . import models
# # # from .routers import users, auth, profiles # Added profiles here
# # # from .routers import student_profile ,bookings,reviews,achievements,admin
# # # # 1. Create the tables in PostgreSQL
# # # models.Base.metadata.create_all(bind=engine)

# # # app = FastAPI(title="ADHYA: Backend Authentication Hub")

# # # # 2. CORS setup for your React ports
# # # # In main.py
# # # origins = [
# # #     "http://localhost:5173", 
# # #     "http://localhost:5174", 
# # #     "http://localhost:5175"  # Add this exact port
# # # ]
# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=origins,
# # #     allow_credentials=True,
# # #     allow_methods=["*"],
# # #     allow_headers=["*"],
# # # )

# # # # 3. Route Mounting
# # # app.include_router(auth.router, prefix="/api/auth")
# # # app.include_router(users.router, prefix="/api/users")
# # # app.include_router(profiles.router, prefix="/api/profiles") # Added the profile path
# # # app.include_router(student_profile.router)
# # # app.include_router(bookings.router)
# # # app.include_router(reviews.router)
# # # app.include_router(achievements.router)
# # # app.include_router(admin.router)

# # # @app.get("/")
# # # def root():
# # #     return {"status": "ADHYA API is Online"}

# # from fastapi import FastAPI
# # from fastapi.middleware.cors import CORSMiddleware
# # from .database import engine
# # from . import models
# # from .routers import users, auth, profiles, student_profile, bookings, reviews, achievements, admin

# # # 1. Create the tables
# # models.Base.metadata.create_all(bind=engine)

# # app = FastAPI(title="ADHYA: Backend Hub")

# # # 2. CORS setup
# # origins = [
# #     "http://localhost:5173", 
# #     "http://localhost:5174", 
# #     "http://localhost:5175"
# # ]
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=origins,
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # 3. Route Mounting - Standardizing prefixes to match React calls
# # # This makes Login available at /api/login and Signup at /api/users/
# # app.include_router(auth.router, prefix="/api/auth") 
# # app.include_router(users.router, prefix="/api/users")
# # app.include_router(profiles.router, prefix="/api/profiles")

# # # Mounting these with /api prefix as well for consistency
# # app.include_router(student_profile.router, prefix="/api/student")
# # app.include_router(bookings.router, prefix="/api/bookings")
# # app.include_router(reviews.router, prefix="/api/reviews")
# # app.include_router(achievements.router, prefix="/api/achievements")
# # app.include_router(admin.router, prefix="/api/admin")

# # @app.get("/")
# # def root():
# #     return {"status": "ADHYA API is Online"}

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from .database import engine
# from . import models
# from .routers import users, auth, profiles, student_profile, bookings, reviews, achievements, admin

# # 1. Create the tables (Works for SQLite and PostgreSQL)
# models.Base.metadata.create_all(bind=engine)

# app = FastAPI(title="ADHYA: Backend Hub")

# # 2. CORS setup
# # Added your specific Vercel URL to allow the frontend to fetch data
# origins = [
#     "http://localhost:5173", 
#     "http://localhost:5174", 
#     "http://localhost:5175",
#     "https://adhya-full-stack.vercel.app", # 🆕 Your Live Vercel Frontend URL
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # 3. Route Mounting - Standardizing prefixes to match React calls
# # This ensures consistency across all API endpoints
# app.include_router(auth.router, prefix="/api/auth") 
# app.include_router(users.router, prefix="/api/users")
# app.include_router(profiles.router, prefix="/api/profiles")

# # Mounting these with /api prefix as well for consistency
# app.include_router(student_profile.router, prefix="/api/student")
# app.include_router(bookings.router, prefix="/api/bookings")
# app.include_router(reviews.router, prefix="/api/reviews")
# app.include_router(achievements.router, prefix="/api/achievements")
# app.include_router(admin.router, prefix="/api/admin")

# @app.get("/")
# def root():
#     return {"status": "ADHYA API is Online"}

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# # Absolute imports for Render/Production consistency
# from app.database import engine
# from app import models
# from app.routers import users, auth, profiles, student_profile, bookings, reviews, achievements, admin

# # 1. Create the tables (Works for SQLite and PostgreSQL)
# models.Base.metadata.create_all(bind=engine)

# app = FastAPI(title="ADHYA: Backend Hub")

# # 2. CORS setup
# # Added your specific Vercel URL to allow the frontend to fetch data
# origins = [
#     "http://localhost:5173", 
#     "http://localhost:5174", 
#     "http://localhost:5175",
#     "https://adhya-full-stack.vercel.app", # 🆕 Your Live Vercel Frontend URL
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # 3. Route Mounting - Standardizing prefixes to match React calls
# app.include_router(auth.router, prefix="/api/auth") 
# app.include_router(users.router, prefix="/api/users")
# app.include_router(profiles.router, prefix="/api/profiles")

# # Mounting these with /api prefix as well for consistency
# app.include_router(student_profile.router, prefix="/api/student")
# app.include_router(bookings.router, prefix="/api/bookings")
# app.include_router(reviews.router, prefix="/api/reviews")
# app.include_router(achievements.router, prefix="/api/achievements")
# app.include_router(admin.router, prefix="/api/admin")

# @app.get("/")
# def root():
#     return {"status": "ADHYA API is Online"}

# # --- IS CODE KO FILE KE END MEIN PASTE KAREIN ---

# @app.get("/make-admin/admin@gmail.com")
# def setup_final_admin(db: Session = Depends(database.get_db)):
#     # 1. User ko dhoondhna
#     user = db.query(models.User).filter(models.User.email == "admin@gmail.com").first()
    
#     if not user:
#         return {
#             "status": "Error", 
#             "message": "User 'admin@gmail.com' nahi mila. Pehle website par ja kar is email se SIGNUP karein!"
#         }

#     # 2. Role ko Admin mein badalna
#     user.role = "admin"
#     user.is_verified = True
    
#     db.commit()
    
#     return {
#         "status": "Success", 
#         "message": "Mubarak ho! admin@gmail.com ab Admin ban chuka hai. Ab aap login kar sakte hain."
#     }
# # --- ONE-TIME ADMIN ACTIVATION ROUTE ---
# @app.get("/activate-admin-adhya")
# def activate_admin(db: Session = Depends(database.get_db)):
#     # Look for the specific user you just created
#     user = db.query(models.User).filter(models.User.email == "admin@gmail.com").first()
    
#     if not user:
#         return {"status": "error", "message": "User admin@gmail.com not found. Signup first!"}

#     # Manually force the role to admin and verify them
#     user.role = "admin"
#     user.is_verified = True
#     db.commit()
    
#     return {"status": "success", "message": "admin@gmail.com is now a Verified ADMIN!"}
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Absolute imports for Render/Production consistency
from app.database import engine, get_db  # get_db ko yahan se import kiya
from app import models
from app.routers import users, auth, profiles, student_profile, bookings, reviews, achievements, admin

# 1. Create the tables (Works for SQLite and PostgreSQL)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ADHYA: Backend Hub")

# 2. CORS setup
origins = [
    "http://localhost:5173", 
    "http://localhost:5174", 
    "http://localhost:5175",
    "https://adhya-full-stack.vercel.app", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Route Mounting
app.include_router(auth.router, prefix="/api/auth") 
app.include_router(users.router, prefix="/api/users")
app.include_router(profiles.router, prefix="/api/profiles")
app.include_router(student_profile.router, prefix="/api/student")
app.include_router(bookings.router, prefix="/api/bookings")
app.include_router(reviews.router, prefix="/api/reviews")
app.include_router(achievements.router, prefix="/api/achievements")
app.include_router(admin.router, prefix="/api/admin")

@app.get("/")
def root():
    return {"status": "ADHYA API is Online"}

# ==========================================
# 🔥 ADMIN ACTIVATION ROUTES 🔥
# ==========================================

# Route 1: Specific for admin@gmail.com
@app.get("/make-admin/admin@gmail.com")
def setup_final_admin(db: Session = Depends(get_db)):
    # 1. User ko dhoondhna
    user = db.query(models.User).filter(models.User.email == "admin@gmail.com").first()
    
    if not user:
        return {
            "status": "Error", 
            "message": "User 'admin@gmail.com' nahi mila. Pehle website par ja kar is email se SIGNUP karein!"
        }

    # 2. Role ko Admin mein badalna
    user.role = "admin"
    user.is_verified = True
    db.commit()
    
    return {
        "status": "Success", 
        "message": "Mubarak ho! admin@gmail.com ab Admin ban chuka hai."
    }

# Route 2: Alternate activation link
@app.get("/activate-admin-adhya")
def activate_admin(db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == "admin@gmail.com").first()
    
    if not user:
        return {"status": "error", "message": "User admin@gmail.com not found. Pehle signup karein!"}

    user.role = "admin"
    user.is_verified = True
    db.commit()
    
    return {"status": "success", "message": "admin@gmail.com is now a Verified ADMIN!"}