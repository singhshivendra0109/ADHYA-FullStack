# # # # from fastapi import APIRouter, Depends, HTTPException, status
# # # # from sqlalchemy.orm import Session
# # # # from .. import models, schemas, oauth2, database
# # # # from sqlalchemy import func
# # # # from typing import List # Required for the list response

# # # # # The prefix ensures all student-related URLs start with /api/students
# # # # router = APIRouter(prefix="", tags=['Student Profiles'])

# # # # @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.StudentProfileOut)
# # # # def create_student_profile(
# # # #     profile: schemas.StudentProfileCreate, 
# # # #     db: Session = Depends(database.get_db),
# # # #     current_user: models.User = Depends(oauth2.get_current_user) 
# # # # ):
# # # #     if current_user.role != "student":
# # # #         raise HTTPException(
# # # #             status_code=status.HTTP_403_FORBIDDEN, 
# # # #             detail="Only students can create a student profile"
# # # #         )

# # # #     existing_profile = db.query(models.StudentProfile).filter(
# # # #         models.StudentProfile.user_id == current_user.id
# # # #     ).first()
    
# # # #     if existing_profile:
# # # #         raise HTTPException(
# # # #             status_code=status.HTTP_400_BAD_REQUEST, 
# # # #             detail="Profile already exists"
# # # #         )

# # # #     new_profile = models.StudentProfile(
# # # #         user_id=current_user.id, 
# # # #         full_name=profile.full_name,
# # # #         grade_class=profile.grade_class,
# # # #         city=profile.city,
# # # #         profile_picture=profile.profile_picture
# # # #     )

# # # #     db.add(new_profile)
# # # #     db.commit()
# # # #     db.refresh(new_profile)
# # # #     return new_profile

# # # # @router.get("/me", response_model=schemas.StudentProfileOut)
# # # # def get_my_profile(
# # # #     db: Session = Depends(database.get_db),
# # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # ):
# # # #     profile = db.query(models.StudentProfile).filter(
# # # #         models.StudentProfile.user_id == current_user.id
# # # #     ).first()
    
# # # #     if not profile:
# # # #         raise HTTPException(status_code=404, detail="Profile not found")
        
# # # #     return profile

# # # # @router.get("/dashboard-stats", status_code=status.HTTP_200_OK)
# # # # def get_student_dashboard_stats(
# # # #     db: Session = Depends(database.get_db),
# # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # ):
# # # #     if current_user.role != "student":
# # # #         raise HTTPException(
# # # #             status_code=status.HTTP_403_FORBIDDEN, 
# # # #             detail="Unauthorized"
# # # #         )

# # # #     active_teachers = db.query(models.Booking).filter(
# # # #         models.Booking.student_id == current_user.id,
# # # #         models.Booking.status == "accepted"
# # # #     ).count()

# # # #     pending_count = db.query(models.Booking).filter(
# # # #         models.Booking.student_id == current_user.id,
# # # #         models.Booking.status == "pending"
# # # #     ).count()

# # # #     reviews_count = db.query(models.Review).filter(
# # # #         models.Review.student_id == current_user.id
# # # #     ).count()

# # # #     return {
# # # #         "total_active_teachers": active_teachers,
# # # #         "pending_requests": pending_count,
# # # #         "total_reviews_given": reviews_count
# # # #     }

# # # # # --- 🆕 ADDED FEATURE 1: My Booking History ---
# # # # @router.get("/my-bookings", response_model=List[schemas.BookingOut])
# # # # def get_student_booking_history(
# # # #     db: Session = Depends(database.get_db),
# # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # ):
# # # #     """Fetch every booking made by the student to show in their dashboard table."""
# # # #     if current_user.role != "student":
# # # #         raise HTTPException(status_code=403, detail="Unauthorized")

# # # #     return db.query(models.Booking).filter(models.Booking.student_id == current_user.id).all()


# # # # # --- 🆕 ADDED FEATURE 3: Cancel a Pending Request ---
# # # # @router.patch("/bookings/{booking_id}/cancel", response_model=schemas.BookingOut)
# # # # def cancel_student_booking(
# # # #     booking_id: int,
# # # #     db: Session = Depends(database.get_db),
# # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # ):
# # # #     """If a student hires the wrong teacher, they can cancel before it's accepted."""
# # # #     booking = db.query(models.Booking).filter(
# # # #         models.Booking.id == booking_id, 
# # # #         models.Booking.student_id == current_user.id
# # # #     ).first()

# # # #     if not booking:
# # # #         raise HTTPException(status_code=404, detail="Booking record not found")
    
# # # #     if booking.status != "pending":
# # # #         raise HTTPException(status_code=400, detail="Only pending requests can be cancelled")

# # # #     booking.status = "cancelled"
# # # #     db.commit()
# # # #     db.refresh(booking)
# # # #     return booking


# # # # @router.patch("/me", response_model=schemas.StudentProfileOut)
# # # # def update_student_profile(
# # # #     profile_update: schemas.StudentProfileUpdate, # Use the new Update schema
# # # #     db: Session = Depends(database.get_db),
# # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # ):
# # # #     profile_query = db.query(models.StudentProfile).filter(models.StudentProfile.user_id == current_user.id)
# # # #     profile = profile_query.first()

# # # #     if not profile:
# # # #         raise HTTPException(status_code=404, detail="Profile not found")

# # # #     # exclude_unset=True is the "secret sauce"
# # # #     # It tells FastAPI to only update the fields you actually typed in Postman.
# # # #     profile_query.update(profile_update.model_dump(exclude_unset=True), synchronize_session=False)
# # # #     db.commit()
    
# # # #     return profile_query.first()

# # # from fastapi import APIRouter, Depends, HTTPException, status
# # # from sqlalchemy.orm import Session
# # # from .. import models, schemas, oauth2, database
# # # from sqlalchemy import func
# # # from typing import List

# # # # Keep prefix empty because main.py handles "/api/student"
# # # router = APIRouter(prefix="", tags=['Student Profiles'])

# # # # 1. FETCH PROFILE: Accessible at GET /api/student/me
# # # @router.get("/me", response_model=schemas.StudentProfileOut)
# # # def get_my_profile(
# # #     db: Session = Depends(database.get_db),
# # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # ):
# # #     profile = db.query(models.StudentProfile).filter(
# # #         models.StudentProfile.user_id == current_user.id
# # #     ).first()
    
# # #     if not profile:
# # #         raise HTTPException(status_code=404, detail="Profile not found")
# # #     return profile

# # # # 2. UPDATE PROFILE: Accessible at PATCH /api/student/me
# # # @router.patch("/me", response_model=schemas.StudentProfileOut)
# # # def update_student_profile(
# # #     profile_update: schemas.StudentProfileUpdate, 
# # #     db: Session = Depends(database.get_db),
# # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # ):
# # #     profile_query = db.query(models.StudentProfile).filter(
# # #         models.StudentProfile.user_id == current_user.id
# # #     )
# # #     profile = profile_query.first()

# # #     if not profile:
# # #         raise HTTPException(status_code=404, detail="Profile not found")

# # #     profile_query.update(profile_update.model_dump(exclude_unset=True), synchronize_session=False)
# # #     db.commit()
# # #     return profile_query.first()

# # # # 3. STATS: Accessible at GET /api/student/dashboard-stats
# # # @router.get("/dashboard-stats", status_code=status.HTTP_200_OK)
# # # def get_student_dashboard_stats(
# # #     db: Session = Depends(database.get_db),
# # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # ):
# # #     if current_user.role != "student":
# # #         raise HTTPException(status_code=403, detail="Unauthorized")

# # #     active_teachers = db.query(models.Booking).filter(
# # #         models.Booking.student_id == current_user.id,
# # #         models.Booking.status == "accepted"
# # #     ).count()

# # #     pending_count = db.query(models.Booking).filter(
# # #         models.Booking.student_id == current_user.id,
# # #         models.Booking.status == "pending"
# # #     ).count()

# # #     reviews_count = db.query(models.Review).filter(
# # #         models.Review.student_id == current_user.id
# # #     ).count()

# # #     return {
# # #         "total_active_teachers": active_teachers,
# # #         "pending_requests": pending_count,
# # #         "total_reviews_given": reviews_count
# # #     }

# # # # 4. BOOKINGS: Accessible at GET /api/student/my-bookings
# # # @router.get("/my-bookings", response_model=List[schemas.BookingOut])
# # # def get_student_booking_history(
# # #     db: Session = Depends(database.get_db),
# # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # ):
# # #     if current_user.role != "student":
# # #         raise HTTPException(status_code=403, detail="Unauthorized")

# # #     return db.query(models.Booking).filter(models.Booking.student_id == current_user.id).all()
# # from fastapi import APIRouter, Depends, HTTPException, status
# # from sqlalchemy.orm import Session
# # from .. import models, schemas, oauth2, database
# # from sqlalchemy import func
# # from typing import List

# # # Keep prefix empty because main.py handles "/api/student"
# # router = APIRouter(prefix="", tags=['Student Profiles'])

# # # 1. CREATE PROFILE: Accessible at POST /api/student/
# # @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.StudentProfileOut)
# # def create_student_profile(
# #     profile: schemas.StudentProfileCreate, 
# #     db: Session = Depends(database.get_db),
# #     current_user: models.User = Depends(oauth2.get_current_user) 
# # ):
# #     # Role Check
# #     if current_user.role != "student":
# #         raise HTTPException(
# #             status_code=status.HTTP_403_FORBIDDEN, 
# #             detail="Only students can create a student profile"
# #         )

# #     # Check if profile already exists to prevent duplicates
# #     existing_profile = db.query(models.StudentProfile).filter(
# #         models.StudentProfile.user_id == current_user.id
# #     ).first()
    
# #     if existing_profile:
# #         raise HTTPException(
# #             status_code=status.HTTP_400_BAD_REQUEST, 
# #             detail="Profile already exists for this user. Use PATCH to update."
# #         )

# #     # Create new profile record
# #     new_profile = models.StudentProfile(
# #         user_id=current_user.id, 
# #         **profile.model_dump() # Unpacks full_name, grade_class, city, profile_picture
# #     )

# #     db.add(new_profile)
# #     db.commit()
# #     db.refresh(new_profile)
# #     return new_profile

# # # 2. FETCH PROFILE: Accessible at GET /api/student/me
# # @router.get("/me", response_model=schemas.StudentProfileOut)
# # def get_my_profile(
# #     db: Session = Depends(database.get_db),
# #     current_user: models.User = Depends(oauth2.get_current_user)
# # ):
# #     profile = db.query(models.StudentProfile).filter(
# #         models.StudentProfile.user_id == current_user.id
# #     ).first()
    
# #     if not profile:
# #         raise HTTPException(status_code=404, detail="Profile not found")
# #     return profile

# # # 3. UPDATE PROFILE: Accessible at PATCH /api/student/me
# # @router.patch("/me", response_model=schemas.StudentProfileOut)
# # def update_student_profile(
# #     profile_update: schemas.StudentProfileUpdate, 
# #     db: Session = Depends(database.get_db),
# #     current_user: models.User = Depends(oauth2.get_current_user)
# # ):
# #     profile_query = db.query(models.StudentProfile).filter(
# #         models.StudentProfile.user_id == current_user.id
# #     )
# #     profile = profile_query.first()

# #     if not profile:
# #         raise HTTPException(status_code=404, detail="Profile not found")

# #     # exclude_unset=True ensures only provided fields are updated
# #     profile_query.update(profile_update.model_dump(exclude_unset=True), synchronize_session=False)
# #     db.commit()
# #     return profile_query.first()

# # # 4. STATS: Accessible at GET /api/student/dashboard-stats
# # @router.get("/dashboard-stats", status_code=status.HTTP_200_OK)
# # def get_student_dashboard_stats(
# #     db: Session = Depends(database.get_db),
# #     current_user: models.User = Depends(oauth2.get_current_user)
# # ):
# #     if current_user.role != "student":
# #         raise HTTPException(status_code=403, detail="Unauthorized")

# #     active_teachers = db.query(models.Booking).filter(
# #         models.Booking.student_id == current_user.id,
# #         models.Booking.status == "accepted"
# #     ).count()

# #     pending_count = db.query(models.Booking).filter(
# #         models.Booking.student_id == current_user.id,
# #         models.Booking.status == "pending"
# #     ).count()

# #     reviews_count = db.query(models.Review).filter(
# #         models.Review.student_id == current_user.id
# #     ).count()

# #     return {
# #         "total_active_teachers": active_teachers,
# #         "pending_requests": pending_count,
# #         "total_reviews_given": reviews_count
# #     }

# # # 5. BOOKINGS: Accessible at GET /api/student/my-bookings
# # @router.get("/my-bookings", response_model=List[schemas.BookingOut])
# # def get_student_booking_history(
# #     db: Session = Depends(database.get_db),
# #     current_user: models.User = Depends(oauth2.get_current_user)
# # ):
# #     if current_user.role != "student":
# #         raise HTTPException(status_code=403, detail="Unauthorized")

# #     return db.query(models.Booking).filter(models.Booking.student_id == current_user.id).all()

# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from .. import models, schemas, oauth2, database
# from sqlalchemy import func
# from typing import List

# # Keep prefix empty because main.py handles "/api/student"
# router = APIRouter(prefix="", tags=['Student Profiles'])

# # 1. CREATE PROFILE: Accessible at POST /api/student/
# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.StudentProfileOut)
# def create_student_profile(
#     profile: schemas.StudentProfileCreate, 
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user) 
# ):
#     # Role Check
#     if current_user.role != "student":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, 
#             detail="Only students can create a student profile"
#         )

#     # Check if profile already exists to prevent duplicates
#     existing_profile = db.query(models.StudentProfile).filter(
#         models.StudentProfile.user_id == current_user.id
#     ).first()
    
#     if existing_profile:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, 
#             detail="Profile already exists for this user. Use PATCH to update."
#         )

#     # Create new profile record
#     new_profile = models.StudentProfile(
#         user_id=current_user.id, 
#         **profile.model_dump() # Unpacks full_name, grade_class, city, profile_picture
#     )

#     db.add(new_profile)
#     db.commit()
#     db.refresh(new_profile)
#     return new_profile

# # 2. FETCH OWN PROFILE: Accessible at GET /api/student/me
# @router.get("/me", response_model=schemas.StudentProfileOut)
# def get_my_profile(
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     profile = db.query(models.StudentProfile).filter(
#         models.StudentProfile.user_id == current_user.id
#     ).first()
    
#     if not profile:
#         raise HTTPException(status_code=404, detail="Profile not found")
#     return profile

# # 3. UPDATE OWN PROFILE: Accessible at PATCH /api/student/me
# @router.patch("/me", response_model=schemas.StudentProfileOut)
# def update_student_profile(
#     profile_update: schemas.StudentProfileUpdate, 
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     profile_query = db.query(models.StudentProfile).filter(
#         models.StudentProfile.user_id == current_user.id
#     )
#     profile = profile_query.first()

#     if not profile:
#         raise HTTPException(status_code=404, detail="Profile not found")

#     # exclude_unset=True ensures only provided fields are updated
#     profile_query.update(profile_update.model_dump(exclude_unset=True), synchronize_session=False)
#     db.commit()
#     return profile_query.first()

# # 4. STATS: Accessible at GET /api/student/dashboard-stats
# @router.get("/dashboard-stats", status_code=status.HTTP_200_OK)
# def get_student_dashboard_stats(
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     if current_user.role != "student":
#         raise HTTPException(status_code=403, detail="Unauthorized")

#     active_teachers = db.query(models.Booking).filter(
#         models.Booking.student_id == current_user.id,
#         models.Booking.status == "accepted"
#     ).count()

#     pending_count = db.query(models.Booking).filter(
#         models.Booking.student_id == current_user.id,
#         models.Booking.status == "pending"
#     ).count()

#     reviews_count = db.query(models.Review).filter(
#         models.Review.student_id == current_user.id
#     ).count()

#     return {
#         "total_active_teachers": active_teachers,
#         "pending_requests": pending_count,
#         "total_reviews_given": reviews_count
#     }

# # 5. BOOKINGS: Accessible at GET /api/student/my-bookings
# @router.get("/my-bookings", response_model=List[schemas.BookingOut])
# def get_student_booking_history(
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     if current_user.role != "student":
#         raise HTTPException(status_code=403, detail="Unauthorized")

#     return db.query(models.Booking).filter(models.Booking.student_id == current_user.id).all()


# # --- 🆕 ADDED: FETCH SPECIFIC STUDENT FOR TEACHER VIEW ---
# # This resolves the 404 error when clicking the student icon in TeacherDashboard
# @router.get("/{user_id}", response_model=schemas.StudentProfileOut)
# def get_student_by_id(
#     user_id: int,
#     db: Session = Depends(database.get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     """Allows teachers to view the profile of a student who requested a booking."""
#     # Logic: Teachers need to see who is applying. We fetch by the user_id provided in the booking.
#     profile = db.query(models.StudentProfile).filter(
#         models.StudentProfile.user_id == user_id
#     ).first()
    
#     if not profile:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, 
#             detail="Student profile data not found. The student may not have completed their setup."
#         )
        
#     return profile
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2, database
from sqlalchemy import func
from typing import List

# Keep prefix empty because main.py handles "/api/student"
router = APIRouter(prefix="", tags=['Student Profiles'])

# --- 1. PUBLIC: FETCH ALL STUDENT NAMES (NEW) ---
# This allows the Landing Page (ReviewSlider/SuccessWall) to map IDs to Names without login
@router.get("/all-names", response_model=List[schemas.StudentProfileOut])
def get_public_student_names(db: Session = Depends(database.get_db)):
    """A public route that only returns basic profile info for UI name mapping."""
    return db.query(models.StudentProfile).all()

# --- 2. CREATE PROFILE ---
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.StudentProfileOut)
def create_student_profile(
    profile: schemas.StudentProfileCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user) 
):
    if current_user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Only students can create a student profile"
        )

    existing_profile = db.query(models.StudentProfile).filter(
        models.StudentProfile.user_id == current_user.id
    ).first()
    
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Profile already exists for this user. Use PATCH to update."
        )

    new_profile = models.StudentProfile(
        user_id=current_user.id, 
        **profile.model_dump()
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

# --- 3. FETCH OWN PROFILE ---
@router.get("/me", response_model=schemas.StudentProfileOut)
def get_my_profile(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    profile = db.query(models.StudentProfile).filter(
        models.StudentProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

# --- 4. UPDATE OWN PROFILE ---
@router.patch("/me", response_model=schemas.StudentProfileOut)
def update_student_profile(
    profile_update: schemas.StudentProfileUpdate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    profile_query = db.query(models.StudentProfile).filter(
        models.StudentProfile.user_id == current_user.id
    )
    profile = profile_query.first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile_query.update(profile_update.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    return profile_query.first()

# --- 5. DASHBOARD STATS ---
@router.get("/dashboard-stats", status_code=status.HTTP_200_OK)
def get_student_dashboard_stats(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Unauthorized")

    active_teachers = db.query(models.Booking).filter(
        models.Booking.student_id == current_user.id,
        models.Booking.status == "accepted"
    ).count()

    pending_count = db.query(models.Booking).filter(
        models.Booking.student_id == current_user.id,
        models.Booking.status == "pending"
    ).count()

    reviews_count = db.query(models.Review).filter(
        models.Review.student_id == current_user.id
    ).count()

    return {
        "total_active_teachers": active_teachers,
        "pending_requests": pending_count,
        "total_reviews_given": reviews_count
    }

# --- 6. BOOKING HISTORY ---
@router.get("/my-bookings", response_model=List[schemas.BookingOut])
def get_student_booking_history(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Unauthorized")

    return db.query(models.Booking).filter(models.Booking.student_id == current_user.id).all()

# --- 7. FETCH SPECIFIC STUDENT (For Admin/Teacher Discovery) ---
@router.get("/{user_id}", response_model=schemas.StudentProfileOut)
def get_student_by_id(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Allows authenticated users (Admins/Teachers) to view a specific student profile."""
    profile = db.query(models.StudentProfile).filter(
        models.StudentProfile.user_id == user_id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Student profile data not found."
        )
        
    return profile