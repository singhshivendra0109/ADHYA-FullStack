

# # # # # # # from fastapi import APIRouter, Depends, HTTPException, status
# # # # # # # from sqlalchemy.orm import Session
# # # # # # # from sqlalchemy import func  # <-- Added for calculations
# # # # # # # from .. import models, schemas, oauth2
# # # # # # # from ..database import get_db


# # # # # # # router = APIRouter(prefix="", tags=['Teacher Profiles'])

# # # # # # # # --- 1. PROFILE CREATION (Unchanged) ---
# # # # # # # @router.post("", response_model=schemas.TeacherProfileOut)
# # # # # # # def create_teacher_profile(
# # # # # # #     profile_data: schemas.TeacherProfileCreate, 
# # # # # # #     db: Session = Depends(get_db), 
# # # # # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # # # # ):
# # # # # # #     if current_user.role != "teacher":
# # # # # # #         raise HTTPException(
# # # # # # #             status_code=status.HTTP_403_FORBIDDEN, 
# # # # # # #             detail="Access Denied: Only teachers can create professional profiles."
# # # # # # #         )

# # # # # # #     existing_profile = db.query(models.TeacherProfile).filter(
# # # # # # #         models.TeacherProfile.user_id == current_user.id
# # # # # # #     ).first()
    
# # # # # # #     if existing_profile:
# # # # # # #         raise HTTPException(
# # # # # # #             status_code=status.HTTP_400_BAD_REQUEST, 
# # # # # # #             detail="A profile already exists for this account."
# # # # # # #         )

# # # # # # #     new_profile = models.TeacherProfile(
# # # # # # #         user_id=current_user.id, 
# # # # # # #         **profile_data.model_dump()
# # # # # # #     )
    
# # # # # # #     db.add(new_profile)
# # # # # # #     db.commit()
# # # # # # #     db.refresh(new_profile)
# # # # # # #     return new_profile

# # # # # # # # --- 2. DISCOVERY (UPDATED WITH RATINGS) ---
# # # # # # # @router.get("/all", response_model=list[schemas.TeacherProfileOut])
# # # # # # # def get_all_teachers(db: Session = Depends(get_db)):
# # # # # # #     """Fetch all teacher profiles with calculated ratings."""
# # # # # # #     profiles = db.query(models.TeacherProfile).all()
    
# # # # # # #     for profile in profiles:
# # # # # # #         # Calculate stats for each teacher
# # # # # # #         stats = db.query(
# # # # # # #             func.avg(models.Review.rating).label('average'),
# # # # # # #             func.count(models.Review.id).label('count')
# # # # # # #         ).filter(models.Review.teacher_id == profile.user_id).first()
        
# # # # # # #         profile.average_rating = round(stats.average or 0.0, 1)
# # # # # # #         profile.total_reviews = stats.count or 0
        
# # # # # # #     return profiles

# # # # # # # # --- 3. TEACHER AVAILABILITY (POST - Unchanged) ---
# # # # # # # @router.post("/availability", response_model=schemas.AvailabilityOut)
# # # # # # # def set_availability(
# # # # # # #     data: schemas.AvailabilityCreate, 
# # # # # # #     db: Session = Depends(get_db),
# # # # # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # # # # ):
# # # # # # #     if current_user.role != "teacher":
# # # # # # #         raise HTTPException(status_code=403, detail="Only teachers can set availability")

# # # # # # #     existing_slot = db.query(models.TeacherAvailability).filter(
# # # # # # #         models.TeacherAvailability.teacher_id == current_user.id,
# # # # # # #         models.TeacherAvailability.month_year == data.month_year,
# # # # # # #         models.TeacherAvailability.time_slot == data.time_slot
# # # # # # #     ).first()

# # # # # # #     if existing_slot:
# # # # # # #         raise HTTPException(status_code=400, detail="This slot is already marked as available")

# # # # # # #     new_slot = models.TeacherAvailability(
# # # # # # #         teacher_id=current_user.id,
# # # # # # #         **data.model_dump()
# # # # # # #     )
# # # # # # #     db.add(new_slot)
# # # # # # #     db.commit()
# # # # # # #     db.refresh(new_slot)
# # # # # # #     return new_slot

# # # # # # # # --- 4. TEACHER AVAILABILITY (GET - Unchanged) ---
# # # # # # # @router.get("/availability/{teacher_id}", response_model=list[schemas.AvailabilityOut])
# # # # # # # def get_teacher_availability(teacher_id: int, month_year: str, db: Session = Depends(get_db)):
# # # # # # #     slots = db.query(models.TeacherAvailability).filter(
# # # # # # #         models.TeacherAvailability.teacher_id == teacher_id,
# # # # # # #         models.TeacherAvailability.month_year == month_year,
# # # # # # #         models.TeacherAvailability.is_active == True
# # # # # # #     ).all()
# # # # # # #     return slots

# # # # # # # # --- 5. SPECIFIC PROFILE (UPDATED WITH RATINGS) ---
# # # # # # # @router.get("/{user_id}", response_model=schemas.TeacherProfileOut)
# # # # # # # def get_teacher_profile(user_id: int, db: Session = Depends(get_db)):
# # # # # # #     profile = db.query(models.TeacherProfile).filter(
# # # # # # #         models.TeacherProfile.user_id == user_id
# # # # # # #     ).first()
    
# # # # # # #     if not profile:
# # # # # # #         raise HTTPException(status_code=404, detail="Profile not found")

# # # # # # #     # Calculate average and count from the reviews table
# # # # # # #     stats = db.query(
# # # # # # #         func.avg(models.Review.rating).label('average'),
# # # # # # #         func.count(models.Review.id).label('count')
# # # # # # #     ).filter(models.Review.teacher_id == user_id).first()

# # # # # # #     profile.average_rating = round(stats.average or 0.0, 1)
# # # # # # #     profile.total_reviews = stats.count or 0
        
# # # # # # #     return profile

# # # # # # from fastapi import APIRouter, Depends, HTTPException, status
# # # # # # from sqlalchemy.orm import Session
# # # # # # from sqlalchemy import func 
# # # # # # from typing import Optional, List # Added Optional for filtering
# # # # # # from .. import models, schemas, oauth2
# # # # # # from ..database import get_db

# # # # # # router = APIRouter(prefix="", tags=['Teacher Profiles'])

# # # # # # # --- 1. PROFILE CREATION (Unchanged) ---
# # # # # # @router.post("", response_model=schemas.TeacherProfileOut)
# # # # # # def create_teacher_profile(
# # # # # #     profile_data: schemas.TeacherProfileCreate, 
# # # # # #     db: Session = Depends(get_db), 
# # # # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # # # ):
# # # # # #     if current_user.role != "teacher":
# # # # # #         raise HTTPException(
# # # # # #             status_code=status.HTTP_403_FORBIDDEN, 
# # # # # #             detail="Access Denied: Only teachers can create professional profiles."
# # # # # #         )

# # # # # #     existing_profile = db.query(models.TeacherProfile).filter(
# # # # # #         models.TeacherProfile.user_id == current_user.id
# # # # # #     ).first()
    
# # # # # #     if existing_profile:
# # # # # #         raise HTTPException(
# # # # # #             status_code=status.HTTP_400_BAD_REQUEST, 
# # # # # #             detail="A profile already exists for this account."
# # # # # #         )

# # # # # #     new_profile = models.TeacherProfile(
# # # # # #         user_id=current_user.id, 
# # # # # #         **profile_data.model_dump()
# # # # # #     )
    
# # # # # #     db.add(new_profile)
# # # # # #     db.commit()
# # # # # #     db.refresh(new_profile)
# # # # # #     return new_profile

# # # # # # # --- 2. DISCOVERY (UPDATED WITH SEARCH & RATINGS) ---
# # # # # # @router.get("/all", response_model=List[schemas.TeacherProfileOut])
# # # # # # def get_all_teachers(
# # # # # #     db: Session = Depends(get_db),
# # # # # #     subject: Optional[str] = None,       # Added filter
# # # # # #     min_price: Optional[float] = None,   # Added filter
# # # # # #     max_price: Optional[float] = None    # Added filter
# # # # # # ):
# # # # # #     """Fetch teacher profiles with optional search and calculated ratings."""
    
# # # # # #     # Start with base query
# # # # # #     query = db.query(models.TeacherProfile)

# # # # # #     # Apply Search Filters
# # # # # #     if subject:
# # # # # #         # ilike handles case-insensitive search (e.g., 'math' matches 'Maths')
# # # # # #         query = query.filter(models.TeacherProfile.subject.ilike(f"%{subject}%"))
    
# # # # # #     if min_price is not None:
# # # # # #         query = query.filter(models.TeacherProfile.monthly_rate >= min_price)
        
# # # # # #     if max_price is not None:
# # # # # #         query = query.filter(models.TeacherProfile.monthly_rate <= max_price)

# # # # # #     profiles = query.all()
    
# # # # # #     for profile in profiles:
# # # # # #         # Calculate stats for each teacher from reviews table
# # # # # #         stats = db.query(
# # # # # #             func.avg(models.Review.rating).label('average'),
# # # # # #             func.count(models.Review.id).label('count')
# # # # # #         ).filter(models.Review.teacher_id == profile.user_id).first()
        
# # # # # #         profile.average_rating = round(stats.average or 0.0, 1)
# # # # # #         profile.total_reviews = stats.count or 0
        
# # # # # #     return profiles

# # # # # # # --- 3. TEACHER AVAILABILITY (POST - Unchanged) ---
# # # # # # @router.post("/availability", response_model=schemas.AvailabilityOut)
# # # # # # def set_availability(
# # # # # #     data: schemas.AvailabilityCreate, 
# # # # # #     db: Session = Depends(get_db),
# # # # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # # # ):
# # # # # #     if current_user.role != "teacher":
# # # # # #         raise HTTPException(status_code=403, detail="Only teachers can set availability")

# # # # # #     existing_slot = db.query(models.TeacherAvailability).filter(
# # # # # #         models.TeacherAvailability.teacher_id == current_user.id,
# # # # # #         models.TeacherAvailability.month_year == data.month_year,
# # # # # #         models.TeacherAvailability.time_slot == data.time_slot
# # # # # #     ).first()

# # # # # #     if existing_slot:
# # # # # #         raise HTTPException(status_code=400, detail="This slot is already marked as available")

# # # # # #     new_slot = models.TeacherAvailability(
# # # # # #         teacher_id=current_user.id,
# # # # # #         **data.model_dump()
# # # # # #     )
# # # # # #     db.add(new_slot)
# # # # # #     db.commit()
# # # # # #     db.refresh(new_slot)
# # # # # #     return new_slot

# # # # # # # --- 4. TEACHER AVAILABILITY (GET - Unchanged) ---
# # # # # # @router.get("/availability/{teacher_id}", response_model=List[schemas.AvailabilityOut])
# # # # # # def get_teacher_availability(teacher_id: int, month_year: str, db: Session = Depends(get_db)):
# # # # # #     slots = db.query(models.TeacherAvailability).filter(
# # # # # #         models.TeacherAvailability.teacher_id == teacher_id,
# # # # # #         models.TeacherAvailability.month_year == month_year,
# # # # # #         models.TeacherAvailability.is_active == True
# # # # # #     ).all()
# # # # # #     return slots

# # # # # # # --- 6. TEACHER ACTION CENTER: MANAGE BOOKINGS ---

# # # # # # @router.get("/bookings", response_model=List[schemas.BookingOut])
# # # # # # def get_incoming_requests(
# # # # # #     db: Session = Depends(get_db),
# # # # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # # # ):
# # # # # #     """Allows teachers to see all students who have requested to hire them."""
# # # # # #     if current_user.role != "teacher":
# # # # # #         raise HTTPException(status_code=403, detail="Only teachers can access this list")
    
# # # # # #     return db.query(models.Booking).filter(models.Booking.teacher_id == current_user.id).all()

# # # # # # @router.patch("/bookings/{booking_id}", response_model=schemas.BookingOut)
# # # # # # def update_hire_request(
# # # # # #     booking_id: int,
# # # # # #     status_update: schemas.BookingStatusUpdate,
# # # # # #     db: Session = Depends(get_db),
# # # # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # # # ):
# # # # # #     """Action to Accept or Reject a student booking."""
# # # # # #     booking = db.query(models.Booking).filter(
# # # # # #         models.Booking.id == booking_id, 
# # # # # #         models.Booking.teacher_id == current_user.id
# # # # # #     ).first()

# # # # # #     if not booking:
# # # # # #         raise HTTPException(status_code=404, detail="Booking request not found")

# # # # # #     # Update status (accepted/rejected)
# # # # # #     booking.status = status_update.status
# # # # # #     db.commit()
# # # # # #     db.refresh(booking)
# # # # # #     return booking


# # # # # # # --- 7. TEACHER DASHBOARD STATS ---

# # # # # # @router.get("/dashboard/stats")
# # # # # # def get_teacher_stats(
# # # # # #     db: Session = Depends(get_db),
# # # # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # # # ):
# # # # # #     """Calculates Earnings, Student Count, and Profile Strength."""
# # # # # #     if current_user.role != "teacher":
# # # # # #         raise HTTPException(status_code=403, detail="Unauthorized")

# # # # # #     # 1. Total Active Students (Accepted Bookings)
# # # # # #     student_count = db.query(models.Booking).filter(
# # # # # #         models.Booking.teacher_id == current_user.id,
# # # # # #         models.Booking.status == "accepted"
# # # # # #     ).count()

# # # # # #     # 2. Total Monthly Earnings (Sum of rates from accepted students)
# # # # # #     # We join with TeacherProfile to get the monthly_rate
# # # # # #     earnings = db.query(func.sum(models.TeacherProfile.monthly_rate)).join(
# # # # # #         models.Booking, models.Booking.teacher_id == models.TeacherProfile.user_id
# # # # # #     ).filter(
# # # # # #         models.Booking.teacher_id == current_user.id,
# # # # # #         models.Booking.status == "accepted"
# # # # # #     ).scalar() or 0

# # # # # #     return {
# # # # # #         "active_students": student_count,
# # # # # #         "monthly_revenue": earnings,
# # # # # #         "pending_requests": db.query(models.Booking).filter(
# # # # # #             models.Booking.teacher_id == current_user.id, 
# # # # # #             models.Booking.status == "pending"
# # # # # #         ).count()
# # # # # #     }


# # # # # # # --- 8. UPDATE TEACHER PROFILE (PATCH) ---
# # # # # # @router.patch("/me", response_model=schemas.TeacherProfileOut)
# # # # # # def update_teacher_profile(
# # # # # #     profile_update: schemas.TeacherProfileUpdate, 
# # # # # #     db: Session = Depends(get_db),
# # # # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # # # ):
# # # # # #     """Allows teachers to update their fees, bio, or subject."""
# # # # # #     if current_user.role != "teacher":
# # # # # #         raise HTTPException(status_code=403, detail="Unauthorized")

# # # # # #     profile_query = db.query(models.TeacherProfile).filter(models.TeacherProfile.user_id == current_user.id)
# # # # # #     profile = profile_query.first()

# # # # # #     if not profile:
# # # # # #         raise HTTPException(status_code=404, detail="Profile not found")

# # # # # #     # Use exclude_unset=True so only provided fields are updated
# # # # # #     profile_query.update(profile_update.model_dump(exclude_unset=True), synchronize_session=False)
# # # # # #     db.commit()
# # # # # #     return profile_query.first()


# # # # # # # --- 9. DELETE AVAILABILITY SLOT (DELETE) ---
# # # # # # @router.delete("/availability/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
# # # # # # def delete_availability(
# # # # # #     slot_id: int,
# # # # # #     db: Session = Depends(get_db),
# # # # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # # # ):
# # # # # #     """Allows teachers to remove a specific time slot."""
# # # # # #     if current_user.role != "teacher":
# # # # # #         raise HTTPException(status_code=403, detail="Unauthorized")

# # # # # #     slot = db.query(models.TeacherAvailability).filter(
# # # # # #         models.TeacherAvailability.id == slot_id,
# # # # # #         models.TeacherAvailability.teacher_id == current_user.id
# # # # # #     ).first()

# # # # # #     if not slot:
# # # # # #         raise HTTPException(status_code=404, detail="Slot not found or you are not the owner")

# # # # # #     db.delete(slot)
# # # # # #     db.commit()
# # # # # #     return None # Returns 204 No Content on success

# # # # # # # --- 5. SPECIFIC PROFILE (UPDATED WITH RATINGS) ---
# # # # # # @router.get("/{user_id}", response_model=schemas.TeacherProfileOut)
# # # # # # def get_teacher_profile(user_id: int, db: Session = Depends(get_db)):
# # # # # #     profile = db.query(models.TeacherProfile).filter(
# # # # # #         models.TeacherProfile.user_id == user_id
# # # # # #     ).first()
    
# # # # # #     if not profile:
# # # # # #         raise HTTPException(status_code=404, detail="Profile not found")

# # # # # #     # Calculate average and count from the reviews table
# # # # # #     stats = db.query(
# # # # # #         func.avg(models.Review.rating).label('average'),
# # # # # #         func.count(models.Review.id).label('count')
# # # # # #     ).filter(models.Review.teacher_id == user_id).first()

# # # # # #     profile.average_rating = round(stats.average or 0.0, 1)
# # # # # #     profile.total_reviews = stats.count or 0
        
# # # # # #     return profile
# # # # # from fastapi import APIRouter, Depends, HTTPException, status
# # # # # from sqlalchemy.orm import Session
# # # # # from sqlalchemy import func 
# # # # # from typing import Optional, List 
# # # # # from .. import models, schemas, oauth2
# # # # # from ..database import get_db

# # # # # router = APIRouter(prefix="", tags=['Teacher Profiles'])

# # # # # # --- 1. PROFILE CREATION ---
# # # # # @router.post("", response_model=schemas.TeacherProfileOut)
# # # # # def create_teacher_profile(
# # # # #     profile_data: schemas.TeacherProfileCreate, 
# # # # #     db: Session = Depends(get_db), 
# # # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # # ):
# # # # #     if current_user.role != "teacher":
# # # # #         raise HTTPException(
# # # # #             status_code=status.HTTP_403_FORBIDDEN, 
# # # # #             detail="Access Denied: Only teachers can create professional profiles."
# # # # #         )

# # # # #     existing_profile = db.query(models.TeacherProfile).filter(
# # # # #         models.TeacherProfile.user_id == current_user.id
# # # # #     ).first()
    
# # # # #     if existing_profile:
# # # # #         raise HTTPException(
# # # # #             status_code=status.HTTP_400_BAD_REQUEST, 
# # # # #             detail="A profile already exists for this account."
# # # # #         )

# # # # #     new_profile = models.TeacherProfile(
# # # # #         user_id=current_user.id, 
# # # # #         **profile_data.model_dump()
# # # # #     )
    
# # # # #     db.add(new_profile)
# # # # #     db.commit()
# # # # #     db.refresh(new_profile)
# # # # #     return new_profile

# # # # # # --- 2. DISCOVERY (SEARCH & RATINGS) ---
# # # # # @router.get("/all", response_model=List[schemas.TeacherProfileOut])
# # # # # def get_all_teachers(
# # # # #     db: Session = Depends(get_db),
# # # # #     subject: Optional[str] = None,
# # # # #     min_price: Optional[float] = None,
# # # # #     max_price: Optional[float] = None
# # # # # ):
# # # # #     query = db.query(models.TeacherProfile)

# # # # #     if subject:
# # # # #         query = query.filter(models.TeacherProfile.subject.ilike(f"%{subject}%"))
    
# # # # #     if min_price is not None:
# # # # #         query = query.filter(models.TeacherProfile.monthly_rate >= min_price)
        
# # # # #     if max_price is not None:
# # # # #         query = query.filter(models.TeacherProfile.monthly_rate <= max_price)

# # # # #     profiles = query.all()
    
# # # # #     for profile in profiles:
# # # # #         stats = db.query(
# # # # #             func.avg(models.Review.rating).label('average'),
# # # # #             func.count(models.Review.id).label('count')
# # # # #         ).filter(models.Review.teacher_id == profile.user_id).first()
        
# # # # #         profile.average_rating = round(stats.average or 0.0, 1)
# # # # #         profile.total_reviews = stats.count or 0
        
# # # # #     return profiles

# # # # # # --- 3. TEACHER AVAILABILITY (POST) ---
# # # # # @router.post("/availability", response_model=schemas.AvailabilityOut)
# # # # # def set_availability(
# # # # #     data: schemas.AvailabilityCreate, 
# # # # #     db: Session = Depends(get_db),
# # # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # # ):
# # # # #     if current_user.role != "teacher":
# # # # #         raise HTTPException(status_code=403, detail="Only teachers can set availability")

# # # # #     existing_slot = db.query(models.TeacherAvailability).filter(
# # # # #         models.TeacherAvailability.teacher_id == current_user.id,
# # # # #         models.TeacherAvailability.month_year == data.month_year,
# # # # #         models.TeacherAvailability.time_slot == data.time_slot
# # # # #     ).first()

# # # # #     if existing_slot:
# # # # #         raise HTTPException(status_code=400, detail="This slot is already marked as available")

# # # # #     new_slot = models.TeacherAvailability(
# # # # #         teacher_id=current_user.id,
# # # # #         **data.model_dump()
# # # # #     )
# # # # #     db.add(new_slot)
# # # # #     db.commit()
# # # # #     db.refresh(new_slot)
# # # # #     return new_slot

# # # # # # --- 4. TEACHER AVAILABILITY (GET) ---
# # # # # @router.get("/availability/{teacher_id}", response_model=List[schemas.AvailabilityOut])
# # # # # def get_teacher_availability(teacher_id: int, month_year: str, db: Session = Depends(get_db)):
# # # # #     slots = db.query(models.TeacherAvailability).filter(
# # # # #         models.TeacherAvailability.teacher_id == teacher_id,
# # # # #         models.TeacherAvailability.month_year == month_year,
# # # # #         models.TeacherAvailability.is_active == True
# # # # #     ).all()
# # # # #     return slots

# # # # # # --- 6. TEACHER ACTION CENTER: MANAGE BOOKINGS ---
# # # # # @router.get("/bookings", response_model=List[schemas.BookingOut])
# # # # # def get_incoming_requests(
# # # # #     db: Session = Depends(get_db),
# # # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # # ):
# # # # #     if current_user.role != "teacher":
# # # # #         raise HTTPException(status_code=403, detail="Only teachers can access this list")
    
# # # # #     return db.query(models.Booking).filter(models.Booking.teacher_id == current_user.id).all()

# # # # # @router.patch("/bookings/{booking_id}", response_model=schemas.BookingOut)
# # # # # def update_hire_request(
# # # # #     booking_id: int,
# # # # #     status_update: schemas.BookingStatusUpdate,
# # # # #     db: Session = Depends(get_db),
# # # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # # ):
# # # # #     booking = db.query(models.Booking).filter(
# # # # #         models.Booking.id == booking_id, 
# # # # #         models.Booking.teacher_id == current_user.id
# # # # #     ).first()

# # # # #     if not booking:
# # # # #         raise HTTPException(status_code=404, detail="Booking request not found")

# # # # #     booking.status = status_update.status
# # # # #     db.commit()
# # # # #     db.refresh(booking)
# # # # #     return booking

# # # # # # --- 7. TEACHER DASHBOARD STATS ---
# # # # # @router.get("/dashboard/stats")
# # # # # def get_teacher_stats(
# # # # #     db: Session = Depends(get_db),
# # # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # # ):
# # # # #     if current_user.role != "teacher":
# # # # #         raise HTTPException(status_code=403, detail="Unauthorized")

# # # # #     student_count = db.query(models.Booking).filter(
# # # # #         models.Booking.teacher_id == current_user.id,
# # # # #         models.Booking.status == "accepted"
# # # # #     ).count()

# # # # #     earnings = db.query(func.sum(models.TeacherProfile.monthly_rate)).join(
# # # # #         models.Booking, models.Booking.teacher_id == models.TeacherProfile.user_id
# # # # #     ).filter(
# # # # #         models.Booking.teacher_id == current_user.id,
# # # # #         models.Booking.status == "accepted"
# # # # #     ).scalar() or 0

# # # # #     return {
# # # # #         "active_students": student_count,
# # # # #         "monthly_revenue": earnings,
# # # # #         "pending_requests": db.query(models.Booking).filter(
# # # # #             models.Booking.teacher_id == current_user.id, 
# # # # #             models.Booking.status == "pending"
# # # # #         ).count()
# # # # #     }

# # # # # # --- 8. UPDATE TEACHER PROFILE (PATCH) ---
# # # # # @router.patch("/me", response_model=schemas.TeacherProfileOut)
# # # # # def update_teacher_profile(
# # # # #     profile_update: schemas.TeacherProfileUpdate, 
# # # # #     db: Session = Depends(get_db),
# # # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # # ):
# # # # #     if current_user.role != "teacher":
# # # # #         raise HTTPException(status_code=403, detail="Unauthorized")

# # # # #     profile_query = db.query(models.TeacherProfile).filter(models.TeacherProfile.user_id == current_user.id)
# # # # #     profile = profile_query.first()

# # # # #     if not profile:
# # # # #         raise HTTPException(status_code=404, detail="Profile not found")

# # # # #     profile_query.update(profile_update.model_dump(exclude_unset=True), synchronize_session=False)
# # # # #     db.commit()
# # # # #     return profile_query.first()

# # # # # # --- 9. DELETE AVAILABILITY SLOT (DELETE) ---
# # # # # @router.delete("/availability/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
# # # # # def delete_availability(
# # # # #     slot_id: int,
# # # # #     db: Session = Depends(get_db),
# # # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # # ):
# # # # #     if current_user.role != "teacher":
# # # # #         raise HTTPException(status_code=403, detail="Unauthorized")

# # # # #     slot = db.query(models.TeacherAvailability).filter(
# # # # #         models.TeacherAvailability.id == slot_id,
# # # # #         models.TeacherAvailability.teacher_id == current_user.id
# # # # #     ).first()

# # # # #     if not slot:
# # # # #         raise HTTPException(status_code=404, detail="Slot not found or you are not the owner")

# # # # #     db.delete(slot)
# # # # #     db.commit()
# # # # #     return None 

# # # # # # --- 5. SPECIFIC PROFILE (SEARCH BY PROFILE ID) ---
# # # # # @router.get("/{user_id}", response_model=schemas.TeacherProfileOut)
# # # # # def get_teacher_profile(user_id: int, db: Session = Depends(get_db)):
# # # # #     profile = db.query(models.TeacherProfile).filter(
# # # # #         models.TeacherProfile.user_id == user_id
# # # # #     ).first()
    
# # # # #     if not profile:
# # # # #         raise HTTPException(status_code=404, detail="Profile not found")

# # # # #     stats = db.query(
# # # # #         func.avg(models.Review.rating).label('average'),
# # # # #         func.count(models.Review.id).label('count')
# # # # #     ).filter(models.Review.teacher_id == user_id).first()

# # # # #     profile.average_rating = round(stats.average or 0.0, 1)
# # # # #     profile.total_reviews = stats.count or 0
        
# # # # #     return profile

# # # # # # --- 10. CRITICAL FIX: SEARCH BY USER ID (NEW) ---
# # # # # @router.get("/user/{u_id}", response_model=schemas.TeacherProfileOut)
# # # # # def get_profile_by_user_id(u_id: int, db: Session = Depends(get_db)):
# # # # #     """Ensures profile loads correctly using User ID for teachers like Shivendra."""
# # # # #     profile = db.query(models.TeacherProfile).filter(models.TeacherProfile.user_id == u_id).first()
    
# # # # #     if not profile:
# # # # #         raise HTTPException(status_code=404, detail="Mentor Profile Not Found")

# # # # #     # Reuse stats calculation logic
# # # # #     stats = db.query(
# # # # #         func.avg(models.Review.rating).label('average'),
# # # # #         func.count(models.Review.id).label('count')
# # # # #     ).filter(models.Review.teacher_id == u_id).first()

# # # # #     profile.average_rating = round(stats.average or 0.0, 1)
# # # # #     profile.total_reviews = stats.count or 0
        
# # # # #     return profile
# # # # from fastapi import APIRouter, Depends, HTTPException, status
# # # # from sqlalchemy.orm import Session
# # # # from sqlalchemy import func 
# # # # from typing import Optional, List 
# # # # from .. import models, schemas, oauth2
# # # # from ..database import get_db

# # # # router = APIRouter(prefix="", tags=['Teacher Profiles'])

# # # # # --- 1. PROFILE CREATION & AUTO-UPDATE (LOGIC UPDATED) ---
# # # # @router.post("", response_model=schemas.TeacherProfileOut)
# # # # def create_teacher_profile(
# # # #     profile_data: schemas.TeacherProfileCreate, 
# # # #     db: Session = Depends(get_db), 
# # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # ):
# # # #     if current_user.role != "teacher":
# # # #         raise HTTPException(
# # # #             status_code=status.HTTP_403_FORBIDDEN, 
# # # #             detail="Access Denied: Only teachers can manage professional profiles."
# # # #         )

# # # #     # Check if profile exists
# # # #     existing_profile_query = db.query(models.TeacherProfile).filter(
# # # #         models.TeacherProfile.user_id == current_user.id
# # # #     )
# # # #     existing_profile = existing_profile_query.first()
    
# # # #     # NEW LOGIC: If profile exists, update it instead of crashing/erroring
# # # #     if existing_profile:
# # # #         existing_profile_query.update(profile_data.model_dump(exclude_unset=True), synchronize_session=False)
# # # #         db.commit()
# # # #         return existing_profile_query.first()

# # # #     # If no profile exists, create a new one
# # # #     new_profile = models.TeacherProfile(
# # # #         user_id=current_user.id, 
# # # #         **profile_data.model_dump()
# # # #     )
    
# # # #     db.add(new_profile)
# # # #     db.commit()
# # # #     db.refresh(new_profile)
# # # #     return new_profile

# # # # # --- 2. DISCOVERY (SEARCH & RATINGS) ---
# # # # @router.get("/all", response_model=List[schemas.TeacherProfileOut])
# # # # def get_all_teachers(
# # # #     db: Session = Depends(get_db),
# # # #     subject: Optional[str] = None,
# # # #     min_price: Optional[float] = None,
# # # #     max_price: Optional[float] = None
# # # # ):
# # # #     query = db.query(models.TeacherProfile)

# # # #     if subject:
# # # #         query = query.filter(models.TeacherProfile.subject.ilike(f"%{subject}%"))
    
# # # #     if min_price is not None:
# # # #         query = query.filter(models.TeacherProfile.monthly_rate >= min_price)
        
# # # #     if max_price is not None:
# # # #         query = query.filter(models.TeacherProfile.monthly_rate <= max_price)

# # # #     profiles = query.all()
    
# # # #     for profile in profiles:
# # # #         stats = db.query(
# # # #             func.avg(models.Review.rating).label('average'),
# # # #             func.count(models.Review.id).label('count')
# # # #         ).filter(models.Review.teacher_id == profile.user_id).first()
        
# # # #         profile.average_rating = round(stats.average or 0.0, 1)
# # # #         profile.total_reviews = stats.count or 0
        
# # # #     return profiles

# # # # # --- 3. TEACHER AVAILABILITY (POST) ---
# # # # @router.post("/availability", response_model=schemas.AvailabilityOut)
# # # # def set_availability(
# # # #     data: schemas.AvailabilityCreate, 
# # # #     db: Session = Depends(get_db),
# # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # ):
# # # #     if current_user.role != "teacher":
# # # #         raise HTTPException(status_code=403, detail="Only teachers can set availability")

# # # #     existing_slot = db.query(models.TeacherAvailability).filter(
# # # #         models.TeacherAvailability.teacher_id == current_user.id,
# # # #         models.TeacherAvailability.month_year == data.month_year,
# # # #         models.TeacherAvailability.time_slot == data.time_slot
# # # #     ).first()

# # # #     if existing_slot:
# # # #         raise HTTPException(status_code=400, detail="This slot is already marked as available")

# # # #     new_slot = models.TeacherAvailability(
# # # #         teacher_id=current_user.id,
# # # #         **data.model_dump()
# # # #     )
# # # #     db.add(new_slot)
# # # #     db.commit()
# # # #     db.refresh(new_slot)
# # # #     return new_slot

# # # # # --- 4. TEACHER AVAILABILITY (GET) ---
# # # # @router.get("/availability/{teacher_id}", response_model=List[schemas.AvailabilityOut])
# # # # def get_teacher_availability(teacher_id: int, month_year: str, db: Session = Depends(get_db)):
# # # #     slots = db.query(models.TeacherAvailability).filter(
# # # #         models.TeacherAvailability.teacher_id == teacher_id,
# # # #         models.TeacherAvailability.month_year == month_year,
# # # #         models.TeacherAvailability.is_active == True
# # # #     ).all()
# # # #     return slots

# # # # # --- 6. TEACHER ACTION CENTER: MANAGE BOOKINGS ---
# # # # @router.get("/bookings", response_model=List[schemas.BookingOut])
# # # # def get_incoming_requests(
# # # #     db: Session = Depends(get_db),
# # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # ):
# # # #     if current_user.role != "teacher":
# # # #         raise HTTPException(status_code=403, detail="Only teachers can access this list")
    
# # # #     return db.query(models.Booking).filter(models.Booking.teacher_id == current_user.id).all()

# # # # @router.patch("/bookings/{booking_id}", response_model=schemas.BookingOut)
# # # # def update_hire_request(
# # # #     booking_id: int,
# # # #     status_update: schemas.BookingStatusUpdate,
# # # #     db: Session = Depends(get_db),
# # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # ):
# # # #     booking = db.query(models.Booking).filter(
# # # #         models.Booking.id == booking_id, 
# # # #         models.Booking.teacher_id == current_user.id
# # # #     ).first()

# # # #     if not booking:
# # # #         raise HTTPException(status_code=404, detail="Booking request not found")

# # # #     booking.status = status_update.status
# # # #     db.commit()
# # # #     db.refresh(booking)
# # # #     return booking

# # # # # --- 7. TEACHER DASHBOARD STATS ---
# # # # @router.get("/dashboard/stats")
# # # # def get_teacher_stats(
# # # #     db: Session = Depends(get_db),
# # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # ):
# # # #     if current_user.role != "teacher":
# # # #         raise HTTPException(status_code=403, detail="Unauthorized")

# # # #     student_count = db.query(models.Booking).filter(
# # # #         models.Booking.teacher_id == current_user.id,
# # # #         models.Booking.status == "accepted"
# # # #     ).count()

# # # #     earnings = db.query(func.sum(models.TeacherProfile.monthly_rate)).join(
# # # #         models.Booking, models.Booking.teacher_id == models.TeacherProfile.user_id
# # # #     ).filter(
# # # #         models.Booking.teacher_id == current_user.id,
# # # #         models.Booking.status == "accepted"
# # # #     ).scalar() or 0

# # # #     return {
# # # #         "active_students": student_count,
# # # #         "monthly_revenue": earnings,
# # # #         "pending_requests": db.query(models.Booking).filter(
# # # #             models.Booking.teacher_id == current_user.id, 
# # # #             models.Booking.status == "pending"
# # # #         ).count()
# # # #     }

# # # # # --- 8. UPDATE TEACHER PROFILE (PATCH) ---
# # # # @router.patch("/me", response_model=schemas.TeacherProfileOut)
# # # # def update_teacher_profile(
# # # #     profile_update: schemas.TeacherProfileUpdate, 
# # # #     db: Session = Depends(get_db),
# # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # ):
# # # #     if current_user.role != "teacher":
# # # #         raise HTTPException(status_code=403, detail="Unauthorized")

# # # #     profile_query = db.query(models.TeacherProfile).filter(models.TeacherProfile.user_id == current_user.id)
# # # #     profile = profile_query.first()

# # # #     if not profile:
# # # #         raise HTTPException(status_code=404, detail="Profile not found")

# # # #     profile_query.update(profile_update.model_dump(exclude_unset=True), synchronize_session=False)
# # # #     db.commit()
# # # #     return profile_query.first()

# # # # # --- 9. DELETE AVAILABILITY SLOT (DELETE) ---
# # # # @router.delete("/availability/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
# # # # def delete_availability(
# # # #     slot_id: int,
# # # #     db: Session = Depends(get_db),
# # # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # # ):
# # # #     if current_user.role != "teacher":
# # # #         raise HTTPException(status_code=403, detail="Unauthorized")

# # # #     slot = db.query(models.TeacherAvailability).filter(
# # # #         models.TeacherAvailability.id == slot_id,
# # # #         models.TeacherAvailability.teacher_id == current_user.id
# # # #     ).first()

# # # #     if not slot:
# # # #         raise HTTPException(status_code=404, detail="Slot not found or you are not the owner")

# # # #     db.delete(slot)
# # # #     db.commit()
# # # #     return None 

# # # # # --- 5. SPECIFIC PROFILE (SEARCH BY PROFILE ID) ---
# # # # @router.get("/{user_id}", response_model=schemas.TeacherProfileOut)
# # # # def get_teacher_profile(user_id: int, db: Session = Depends(get_db)):
# # # #     profile = db.query(models.TeacherProfile).filter(
# # # #         models.TeacherProfile.user_id == user_id
# # # #     ).first()
    
# # # #     if not profile:
# # # #         raise HTTPException(status_code=404, detail="Profile not found")

# # # #     stats = db.query(
# # # #         func.avg(models.Review.rating).label('average'),
# # # #         func.count(models.Review.id).label('count')
# # # #     ).filter(models.Review.teacher_id == user_id).first()

# # # #     profile.average_rating = round(stats.average or 0.0, 1)
# # # #     profile.total_reviews = stats.count or 0
        
# # # #     return profile

# # # # # --- 10. CRITICAL FIX: SEARCH BY USER ID (NEW) ---
# # # # @router.get("/user/{u_id}", response_model=schemas.TeacherProfileOut)
# # # # def get_profile_by_user_id(u_id: int, db: Session = Depends(get_db)):
# # # #     profile = db.query(models.TeacherProfile).filter(models.TeacherProfile.user_id == u_id).first()
    
# # # #     if not profile:
# # # #         raise HTTPException(status_code=404, detail="Mentor Profile Not Found")

# # # #     stats = db.query(
# # # #         func.avg(models.Review.rating).label('average'),
# # # #         func.count(models.Review.id).label('count')
# # # #     ).filter(models.Review.teacher_id == u_id).first()

# # # #     profile.average_rating = round(stats.average or 0.0, 1)
# # # #     profile.total_reviews = stats.count or 0
        
# # # #     return profile
# # # from fastapi import APIRouter, Depends, HTTPException, status
# # # from sqlalchemy.orm import Session
# # # from sqlalchemy import func 
# # # from typing import Optional, List 
# # # from .. import models, schemas, oauth2
# # # from ..database import get_db

# # # router = APIRouter(prefix="", tags=['Teacher Profiles'])

# # # # --- 1. PROFILE CREATION & AUTO-UPDATE (UPSERT) ---
# # # @router.post("", response_model=schemas.TeacherProfileOut)
# # # def create_teacher_profile(
# # #     profile_data: schemas.TeacherProfileCreate, 
# # #     db: Session = Depends(get_db), 
# # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # ):
# # #     if current_user.role != "teacher":
# # #         raise HTTPException(
# # #             status_code=status.HTTP_403_FORBIDDEN, 
# # #             detail="Access Denied: Only teachers can manage professional profiles."
# # #         )

# # #     # Check if profile exists
# # #     existing_profile_query = db.query(models.TeacherProfile).filter(
# # #         models.TeacherProfile.user_id == current_user.id
# # #     )
# # #     existing_profile = existing_profile_query.first()
    
# # #     # If profile exists, update it
# # #     if existing_profile:
# # #         existing_profile_query.update(profile_data.model_dump(exclude_unset=True), synchronize_session=False)
# # #         db.commit()
# # #         return existing_profile_query.first()

# # #     # If no profile exists, create a new one
# # #     new_profile = models.TeacherProfile(
# # #         user_id=current_user.id, 
# # #         **profile_data.model_dump()
# # #     )
    
# # #     db.add(new_profile)
# # #     db.commit()
# # #     db.refresh(new_profile)
# # #     return new_profile

# # # # --- 11. DASHBOARD DATA FETCH (FIXES 422 ERROR) ---
# # # @router.get("/me", response_model=schemas.TeacherProfileOut)
# # # def get_my_own_profile(
# # #     db: Session = Depends(get_db), 
# # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # ):
# # #     """Specifically for the Teacher Dashboard to fetch their own profile safely."""
# # #     profile = db.query(models.TeacherProfile).filter(
# # #         models.TeacherProfile.user_id == current_user.id
# # #     ).first()
    
# # #     if not profile:
# # #         # Return a 404 so the Frontend knows to show the 'Create Profile' modal
# # #         raise HTTPException(status_code=404, detail="Profile not found")

# # #     # Calculate real-time ratings
# # #     stats = db.query(
# # #         func.avg(models.Review.rating).label('average'),
# # #         func.count(models.Review.id).label('count')
# # #     ).filter(models.Review.teacher_id == current_user.id).first()

# # #     profile.average_rating = round(stats.average or 0.0, 1)
# # #     profile.total_reviews = stats.count or 0
        
# # #     return profile

# # # # --- 2. DISCOVERY (SEARCH & RATINGS) ---
# # # @router.get("/all", response_model=List[schemas.TeacherProfileOut])
# # # def get_all_teachers(
# # #     db: Session = Depends(get_db),
# # #     subject: Optional[str] = None,
# # #     min_price: Optional[float] = None,
# # #     max_price: Optional[float] = None
# # # ):
# # #     query = db.query(models.TeacherProfile)

# # #     if subject:
# # #         query = query.filter(models.TeacherProfile.subject.ilike(f"%{subject}%"))
    
# # #     if min_price is not None:
# # #         query = query.filter(models.TeacherProfile.monthly_rate >= min_price)
        
# # #     if max_price is not None:
# # #         query = query.filter(models.TeacherProfile.monthly_rate <= max_price)

# # #     profiles = query.all()
    
# # #     for profile in profiles:
# # #         stats = db.query(
# # #             func.avg(models.Review.rating).label('average'),
# # #             func.count(models.Review.id).label('count')
# # #         ).filter(models.Review.teacher_id == profile.user_id).first()
        
# # #         profile.average_rating = round(stats.average or 0.0, 1)
# # #         profile.total_reviews = stats.count or 0
        
# # #     return profiles

# # # # --- 3. TEACHER AVAILABILITY (POST) ---
# # # @router.post("/availability", response_model=schemas.AvailabilityOut)
# # # def set_availability(
# # #     data: schemas.AvailabilityCreate, 
# # #     db: Session = Depends(get_db),
# # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # ):
# # #     if current_user.role != "teacher":
# # #         raise HTTPException(status_code=403, detail="Only teachers can set availability")

# # #     existing_slot = db.query(models.TeacherAvailability).filter(
# # #         models.TeacherAvailability.teacher_id == current_user.id,
# # #         models.TeacherAvailability.month_year == data.month_year,
# # #         models.TeacherAvailability.time_slot == data.time_slot
# # #     ).first()

# # #     if existing_slot:
# # #         raise HTTPException(status_code=400, detail="This slot is already marked as available")

# # #     new_slot = models.TeacherAvailability(
# # #         teacher_id=current_user.id,
# # #         **data.model_dump()
# # #     )
# # #     db.add(new_slot)
# # #     db.commit()
# # #     db.refresh(new_slot)
# # #     return new_slot

# # # # --- 4. TEACHER AVAILABILITY (GET) ---
# # # @router.get("/availability/{teacher_id}", response_model=List[schemas.AvailabilityOut])
# # # def get_teacher_availability(teacher_id: int, month_year: str, db: Session = Depends(get_db)):
# # #     slots = db.query(models.TeacherAvailability).filter(
# # #         models.TeacherAvailability.teacher_id == teacher_id,
# # #         models.TeacherAvailability.month_year == month_year,
# # #         models.TeacherAvailability.is_active == True
# # #     ).all()
# # #     return slots

# # # # --- 6. TEACHER ACTION CENTER: MANAGE BOOKINGS ---
# # # @router.get("/bookings", response_model=List[schemas.BookingOut])
# # # def get_incoming_requests(
# # #     db: Session = Depends(get_db),
# # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # ):
# # #     if current_user.role != "teacher":
# # #         raise HTTPException(status_code=403, detail="Only teachers can access this list")
    
# # #     return db.query(models.Booking).filter(models.Booking.teacher_id == current_user.id).all()

# # # @router.patch("/bookings/{booking_id}", response_model=schemas.BookingOut)
# # # def update_hire_request(
# # #     booking_id: int,
# # #     status_update: schemas.BookingStatusUpdate,
# # #     db: Session = Depends(get_db),
# # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # ):
# # #     booking = db.query(models.Booking).filter(
# # #         models.Booking.id == booking_id, 
# # #         models.Booking.teacher_id == current_user.id
# # #     ).first()

# # #     if not booking:
# # #         raise HTTPException(status_code=404, detail="Booking request not found")

# # #     booking.status = status_update.status
# # #     db.commit()
# # #     db.refresh(booking)
# # #     return booking

# # # # --- 7. TEACHER DASHBOARD STATS ---
# # # @router.get("/dashboard/stats")
# # # def get_teacher_stats(
# # #     db: Session = Depends(get_db),
# # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # ):
# # #     if current_user.role != "teacher":
# # #         raise HTTPException(status_code=403, detail="Unauthorized")

# # #     student_count = db.query(models.Booking).filter(
# # #         models.Booking.teacher_id == current_user.id,
# # #         models.Booking.status == "accepted"
# # #     ).count()

# # #     earnings = db.query(func.sum(models.TeacherProfile.monthly_rate)).join(
# # #         models.Booking, models.Booking.teacher_id == models.TeacherProfile.user_id
# # #     ).filter(
# # #         models.Booking.teacher_id == current_user.id,
# # #         models.Booking.status == "accepted"
# # #     ).scalar() or 0

# # #     return {
# # #         "active_students": student_count,
# # #         "monthly_revenue": earnings,
# # #         "pending_requests": db.query(models.Booking).filter(
# # #             models.Booking.teacher_id == current_user.id, 
# # #             models.Booking.status == "pending"
# # #         ).count()
# # #     }

# # # # --- 8. UPDATE TEACHER PROFILE (PATCH) ---
# # # @router.patch("/me", response_model=schemas.TeacherProfileOut)
# # # def update_teacher_profile(
# # #     profile_update: schemas.TeacherProfileUpdate, 
# # #     db: Session = Depends(get_db),
# # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # ):
# # #     if current_user.role != "teacher":
# # #         raise HTTPException(status_code=403, detail="Unauthorized")

# # #     profile_query = db.query(models.TeacherProfile).filter(models.TeacherProfile.user_id == current_user.id)
# # #     profile = profile_query.first()

# # #     if not profile:
# # #         raise HTTPException(status_code=404, detail="Profile not found")

# # #     profile_query.update(profile_update.model_dump(exclude_unset=True), synchronize_session=False)
# # #     db.commit()
# # #     return profile_query.first()

# # # # --- 9. DELETE AVAILABILITY SLOT (DELETE) ---
# # # @router.delete("/availability/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
# # # def delete_availability(
# # #     slot_id: int,
# # #     db: Session = Depends(get_db),
# # #     current_user: models.User = Depends(oauth2.get_current_user)
# # # ):
# # #     if current_user.role != "teacher":
# # #         raise HTTPException(status_code=403, detail="Unauthorized")

# # #     slot = db.query(models.TeacherAvailability).filter(
# # #         models.TeacherAvailability.id == slot_id,
# # #         models.TeacherAvailability.teacher_id == current_user.id
# # #     ).first()

# # #     if not slot:
# # #         raise HTTPException(status_code=404, detail="Slot not found or you are not the owner")

# # #     db.delete(slot)
# # #     db.commit()
# # #     return None 

# # # # --- 5. SPECIFIC PROFILE (SEARCH BY PROFILE ID) ---
# # # @router.get("/{user_id}", response_model=schemas.TeacherProfileOut)
# # # def get_teacher_profile(user_id: int, db: Session = Depends(get_db)):
# # #     profile = db.query(models.TeacherProfile).filter(
# # #         models.TeacherProfile.user_id == user_id
# # #     ).first()
    
# # #     if not profile:
# # #         raise HTTPException(status_code=404, detail="Profile not found")

# # #     stats = db.query(
# # #         func.avg(models.Review.rating).label('average'),
# # #         func.count(models.Review.id).label('count')
# # #     ).filter(models.Review.teacher_id == user_id).first()

# # #     profile.average_rating = round(stats.average or 0.0, 1)
# # #     profile.total_reviews = stats.count or 0
        
# # #     return profile

# # # # --- 10. CRITICAL FIX: SEARCH BY USER ID ---
# # # @router.get("/user/{u_id}", response_model=schemas.TeacherProfileOut)
# # # def get_profile_by_user_id(u_id: int, db: Session = Depends(get_db)):
# # #     profile = db.query(models.TeacherProfile).filter(models.TeacherProfile.user_id == u_id).first()
    
# # #     if not profile:
# # #         raise HTTPException(status_code=404, detail="Mentor Profile Not Found")

# # #     stats = db.query(
# # #         func.avg(models.Review.rating).label('average'),
# # #         func.count(models.Review.id).label('count')
# # #     ).filter(models.Review.teacher_id == u_id).first()

# # #     profile.average_rating = round(stats.average or 0.0, 1)
# # #     profile.total_reviews = stats.count or 0
        
# # #     return profile

# # from fastapi import APIRouter, Depends, HTTPException, status
# # from sqlalchemy.orm import Session
# # from sqlalchemy import func 
# # from typing import Optional, List 
# # from .. import models, schemas, oauth2
# # from ..database import get_db

# # router = APIRouter(prefix="", tags=['Teacher Profiles'])

# # # --- 1. PROFILE CREATION & AUTO-UPDATE (UPSERT) ---
# # @router.post("", response_model=schemas.TeacherProfileOut)
# # def create_teacher_profile(
# #     profile_data: schemas.TeacherProfileCreate, 
# #     db: Session = Depends(get_db), 
# #     current_user: models.User = Depends(oauth2.get_current_user)
# # ):
# #     if current_user.role != "teacher":
# #         raise HTTPException(
# #             status_code=status.HTTP_403_FORBIDDEN, 
# #             detail="Access Denied: Only teachers can manage professional profiles."
# #         )

# #     existing_profile_query = db.query(models.TeacherProfile).filter(
# #         models.TeacherProfile.user_id == current_user.id
# #     )
# #     existing_profile = existing_profile_query.first()
    
# #     if existing_profile:
# #         existing_profile_query.update(profile_data.model_dump(exclude_unset=True), synchronize_session=False)
# #         db.commit()
# #         return existing_profile_query.first()

# #     new_profile = models.TeacherProfile(
# #         user_id=current_user.id, 
# #         **profile_data.model_dump()
# #     )
    
# #     db.add(new_profile)
# #     db.commit()
# #     db.refresh(new_profile)
# #     return new_profile

# # # --- 2. DISCOVERY: GET ALL VERIFIED TEACHERS (UPDATED WITH JOIN) ---
# # @router.get("/all", response_model=List[schemas.TeacherProfileOut])
# # def get_all_teachers(
# #     db: Session = Depends(get_db),
# #     subject: Optional[str] = None,
# #     min_price: Optional[float] = None,
# #     max_price: Optional[float] = None
# # ):
# #     # Perform a JOIN with User to get the is_verified status
# #     query = db.query(
# #         models.TeacherProfile,
# #         models.User.is_verified
# #     ).join(
# #         models.User, models.TeacherProfile.user_id == models.User.id
# #     )

# #     if subject:
# #         query = query.filter(models.TeacherProfile.subject.ilike(f"%{subject}%"))
    
# #     if min_price is not None:
# #         query = query.filter(models.TeacherProfile.monthly_rate >= min_price)
        
# #     if max_price is not None:
# #         query = query.filter(models.TeacherProfile.monthly_rate <= max_price)

# #     results = query.all()
    
# #     final_profiles = []
# #     for profile_obj, is_verified in results:
# #         # Calculate review stats
# #         stats = db.query(
# #             func.avg(models.Review.rating).label('average'),
# #             func.count(models.Review.id).label('count')
# #         ).filter(models.Review.teacher_id == profile_obj.user_id).first()
        
# #         # Build the schema response
# #         p_data = schemas.TeacherProfileOut.model_validate(profile_obj)
# #         p_data.is_verified = is_verified
# #         p_data.average_rating = round(stats.average or 0.0, 1)
# #         p_data.total_reviews = stats.count or 0
# #         final_profiles.append(p_data)
        
# #     return final_profiles

# # # --- 3. TEACHER DASHBOARD: FETCH OWN PROFILE Safely ---
# # @router.get("/me", response_model=schemas.TeacherProfileOut)
# # def get_my_own_profile(
# #     db: Session = Depends(get_db), 
# #     current_user: models.User = Depends(oauth2.get_current_user)
# # ):
# #     profile = db.query(models.TeacherProfile).filter(
# #         models.TeacherProfile.user_id == current_user.id
# #     ).first()
    
# #     if not profile:
# #         raise HTTPException(status_code=404, detail="Profile not found")

# #     stats = db.query(
# #         func.avg(models.Review.rating).label('average'),
# #         func.count(models.Review.id).label('count')
# #     ).filter(models.Review.teacher_id == current_user.id).first()

# #     p_data = schemas.TeacherProfileOut.model_validate(profile)
# #     p_data.is_verified = current_user.is_verified
# #     p_data.average_rating = round(stats.average or 0.0, 1)
# #     p_data.total_reviews = stats.count or 0
        
# #     return p_data

# # # --- 4. AVAILABILITY: POST ---
# # @router.post("/availability", response_model=schemas.AvailabilityOut)
# # def set_availability(
# #     data: schemas.AvailabilityCreate, 
# #     db: Session = Depends(get_db),
# #     current_user: models.User = Depends(oauth2.get_current_user)
# # ):
# #     if current_user.role != "teacher":
# #         raise HTTPException(status_code=403, detail="Only teachers can set availability")

# #     existing_slot = db.query(models.TeacherAvailability).filter(
# #         models.TeacherAvailability.teacher_id == current_user.id,
# #         models.TeacherAvailability.month_year == data.month_year,
# #         models.TeacherAvailability.time_slot == data.time_slot
# #     ).first()

# #     if existing_slot:
# #         raise HTTPException(status_code=400, detail="This slot is already marked as available")

# #     new_slot = models.TeacherAvailability(
# #         teacher_id=current_user.id,
# #         **data.model_dump()
# #     )
# #     db.add(new_slot)
# #     db.commit()
# #     db.refresh(new_slot)
# #     return new_slot

# # # --- 5. AVAILABILITY: GET ---
# # @router.get("/availability/{teacher_id}", response_model=List[schemas.AvailabilityOut])
# # def get_teacher_availability(teacher_id: int, month_year: str, db: Session = Depends(get_db)):
# #     slots = db.query(models.TeacherAvailability).filter(
# #         models.TeacherAvailability.teacher_id == teacher_id,
# #         models.TeacherAvailability.month_year == month_year,
# #         models.TeacherAvailability.is_active == True
# #     ).all()
# #     return slots

# # # --- 6. MANAGE BOOKINGS ---
# # @router.get("/bookings", response_model=List[schemas.BookingOut])
# # def get_incoming_requests(
# #     db: Session = Depends(get_db),
# #     current_user: models.User = Depends(oauth2.get_current_user)
# # ):
# #     if current_user.role != "teacher":
# #         raise HTTPException(status_code=403, detail="Only teachers can access this list")
    
# #     return db.query(models.Booking).filter(models.Booking.teacher_id == current_user.id).all()

# # @router.patch("/bookings/{booking_id}", response_model=schemas.BookingOut)
# # def update_hire_request(
# #     booking_id: int,
# #     status_update: schemas.BookingStatusUpdate,
# #     db: Session = Depends(get_db),
# #     current_user: models.User = Depends(oauth2.get_current_user)
# # ):
# #     booking = db.query(models.Booking).filter(
# #         models.Booking.id == booking_id, 
# #         models.Booking.teacher_id == current_user.id
# #     ).first()

# #     if not booking:
# #         raise HTTPException(status_code=404, detail="Booking request not found")

# #     booking.status = status_update.status
# #     db.commit()
# #     db.refresh(booking)
# #     return booking

# # # --- 7. TEACHER DASHBOARD STATS ---
# # @router.get("/dashboard/stats")
# # def get_teacher_stats(
# #     db: Session = Depends(get_db),
# #     current_user: models.User = Depends(oauth2.get_current_user)
# # ):
# #     if current_user.role != "teacher":
# #         raise HTTPException(status_code=403, detail="Unauthorized")

# #     student_count = db.query(models.Booking).filter(
# #         models.Booking.teacher_id == current_user.id,
# #         models.Booking.status == "accepted"
# #     ).count()

# #     earnings = db.query(func.sum(models.TeacherProfile.monthly_rate)).join(
# #         models.Booking, models.Booking.teacher_id == models.TeacherProfile.user_id
# #     ).filter(
# #         models.Booking.teacher_id == current_user.id,
# #         models.Booking.status == "accepted"
# #     ).scalar() or 0

# #     return {
# #         "active_students": student_count,
# #         "monthly_revenue": earnings,
# #         "pending_requests": db.query(models.Booking).filter(
# #             models.Booking.teacher_id == current_user.id, 
# #             models.Booking.status == "pending"
# #         ).count()
# #     }

# # # --- 8. DELETE AVAILABILITY SLOT ---
# # @router.delete("/availability/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
# # def delete_availability(
# #     slot_id: int,
# #     db: Session = Depends(get_db),
# #     current_user: models.User = Depends(oauth2.get_current_user)
# # ):
# #     if current_user.role != "teacher":
# #         raise HTTPException(status_code=403, detail="Unauthorized")

# #     slot = db.query(models.TeacherAvailability).filter(
# #         models.TeacherAvailability.id == slot_id,
# #         models.TeacherAvailability.teacher_id == current_user.id
# #     ).first()

# #     if not slot:
# #         raise HTTPException(status_code=404, detail="Slot not found or you are not the owner")

# #     db.delete(slot)
# #     db.commit()
# #     return None 

# # # --- 9. SPECIFIC PROFILE BY USER ID (CRITICAL FOR UI) ---
# # @router.get("/user/{u_id}", response_model=schemas.TeacherProfileOut)
# # def get_profile_by_user_id(u_id: int, db: Session = Depends(get_db)):
# #     result = db.query(
# #         models.TeacherProfile,
# #         models.User.is_verified
# #     ).join(
# #         models.User, models.TeacherProfile.user_id == models.User.id
# #     ).filter(models.TeacherProfile.user_id == u_id).first()
    
# #     if not result:
# #         raise HTTPException(status_code=404, detail="Mentor Profile Not Found")

# #     profile_obj, is_verified = result

# #     stats = db.query(
# #         func.avg(models.Review.rating).label('average'),
# #         func.count(models.Review.id).label('count')
# #     ).filter(models.Review.teacher_id == u_id).first()

# #     p_data = schemas.TeacherProfileOut.model_validate(profile_obj)
# #     p_data.is_verified = is_verified
# #     p_data.average_rating = round(stats.average or 0.0, 1)
# #     p_data.total_reviews = stats.count or 0
        
# #     return p_data
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from sqlalchemy import func 
# from typing import Optional, List 
# from .. import models, schemas, oauth2
# from ..database import get_db

# router = APIRouter(prefix="", tags=['Teacher Profiles'])

# # --- 1. PROFILE CREATION & AUTO-UPDATE (UPSERT) ---
# @router.post("", response_model=schemas.TeacherProfileOut)
# def create_teacher_profile(
#     profile_data: schemas.TeacherProfileCreate, 
#     db: Session = Depends(get_db), 
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     if current_user.role != "teacher":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, 
#             detail="Access Denied: Only teachers can manage professional profiles."
#         )

#     existing_profile_query = db.query(models.TeacherProfile).filter(
#         models.TeacherProfile.user_id == current_user.id
#     )
#     existing_profile = existing_profile_query.first()
    
#     if existing_profile:
#         existing_profile_query.update(profile_data.model_dump(exclude_unset=True), synchronize_session=False)
#         db.commit()
#         return existing_profile_query.first()

#     new_profile = models.TeacherProfile(
#         user_id=current_user.id, 
#         **profile_data.model_dump()
#     )
    
#     db.add(new_profile)
#     db.commit()
#     db.refresh(new_profile)
#     return new_profile

# # --- 2. DISCOVERY: GET ONLY VERIFIED TEACHERS (UPDATED LOGIC) ---
# @router.get("/all", response_model=List[schemas.TeacherProfileOut])
# def get_all_teachers(
#     db: Session = Depends(get_db),
#     subject: Optional[str] = None,
#     min_price: Optional[float] = None,
#     max_price: Optional[float] = None
# ):
#     """
#     Fetch teacher profiles. 
#     CRITICAL: Only returns profiles where the linked User is_verified == True.
#     """
#     # We JOIN with the User table to check verification status
#     query = db.query(
#         models.TeacherProfile,
#         models.User.is_verified
#     ).join(
#         models.User, models.TeacherProfile.user_id == models.User.id
#     ).filter(
#         models.User.is_verified == True # <--- SECURE FILTER AT DATABASE LEVEL
#     )

#     if subject:
#         query = query.filter(models.TeacherProfile.subject.ilike(f"%{subject}%"))
    
#     if min_price is not None:
#         query = query.filter(models.TeacherProfile.monthly_rate >= min_price)
        
#     if max_price is not None:
#         query = query.filter(models.TeacherProfile.monthly_rate <= max_price)

#     results = query.all()
    
#     final_profiles = []
#     for profile_obj, is_verified in results:
#         # Calculate real-time rating stats
#         stats = db.query(
#             func.avg(models.Review.rating).label('average'),
#             func.count(models.Review.id).label('count')
#         ).filter(models.Review.teacher_id == profile_obj.user_id).first()
        
#         # Build the schema response
#         p_data = schemas.TeacherProfileOut.model_validate(profile_obj)
#         p_data.is_verified = is_verified
#         p_data.average_rating = round(stats.average or 0.0, 1)
#         p_data.total_reviews = stats.count or 0
#         final_profiles.append(p_data)
        
#     return final_profiles

# # --- 3. TEACHER DASHBOARD DATA FETCH ---
# @router.get("/me", response_model=schemas.TeacherProfileOut)
# def get_my_own_profile(
#     db: Session = Depends(get_db), 
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     profile = db.query(models.TeacherProfile).filter(
#         models.TeacherProfile.user_id == current_user.id
#     ).first()
    
#     if not profile:
#         raise HTTPException(status_code=404, detail="Profile not found")

#     stats = db.query(
#         func.avg(models.Review.rating).label('average'),
#         func.count(models.Review.id).label('count')
#     ).filter(models.Review.teacher_id == current_user.id).first()

#     p_data = schemas.TeacherProfileOut.model_validate(profile)
#     p_data.is_verified = current_user.is_verified
#     p_data.average_rating = round(stats.average or 0.0, 1)
#     p_data.total_reviews = stats.count or 0
        
#     return p_data

# # --- 4. AVAILABILITY: POST ---
# @router.post("/availability", response_model=schemas.AvailabilityOut)
# def set_availability(
#     data: schemas.AvailabilityCreate, 
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     if current_user.role != "teacher":
#         raise HTTPException(status_code=403, detail="Only teachers can set availability")

#     existing_slot = db.query(models.TeacherAvailability).filter(
#         models.TeacherAvailability.teacher_id == current_user.id,
#         models.TeacherAvailability.month_year == data.month_year,
#         models.TeacherAvailability.time_slot == data.time_slot
#     ).first()

#     if existing_slot:
#         raise HTTPException(status_code=400, detail="This slot is already marked as available")

#     new_slot = models.TeacherAvailability(
#         teacher_id=current_user.id,
#         **data.model_dump()
#     )
#     db.add(new_slot)
#     db.commit()
#     db.refresh(new_slot)
#     return new_slot

# # --- 5. AVAILABILITY: GET ---
# @router.get("/availability/{teacher_id}", response_model=List[schemas.AvailabilityOut])
# def get_teacher_availability(teacher_id: int, month_year: str, db: Session = Depends(get_db)):
#     slots = db.query(models.TeacherAvailability).filter(
#         models.TeacherAvailability.teacher_id == teacher_id,
#         models.TeacherAvailability.month_year == month_year,
#         models.TeacherAvailability.is_active == True
#     ).all()
#     return slots

# # --- 6. MANAGE BOOKINGS ---
# @router.get("/bookings", response_model=List[schemas.BookingOut])
# def get_incoming_requests(
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     if current_user.role != "teacher":
#         raise HTTPException(status_code=403, detail="Only teachers can access this list")
    
#     return db.query(models.Booking).filter(models.Booking.teacher_id == current_user.id).all()

# @router.patch("/bookings/{booking_id}", response_model=schemas.BookingOut)
# def update_hire_request(
#     booking_id: int,
#     status_update: schemas.BookingStatusUpdate,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     booking = db.query(models.Booking).filter(
#         models.Booking.id == booking_id, 
#         models.Booking.teacher_id == current_user.id
#     ).first()

#     if not booking:
#         raise HTTPException(status_code=404, detail="Booking request not found")

#     booking.status = status_update.status
#     db.commit()
#     db.refresh(booking)
#     return booking

# # --- 7. TEACHER DASHBOARD STATS ---
# @router.get("/dashboard/stats")
# def get_teacher_stats(
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     if current_user.role != "teacher":
#         raise HTTPException(status_code=403, detail="Unauthorized")

#     student_count = db.query(models.Booking).filter(
#         models.Booking.teacher_id == current_user.id,
#         models.Booking.status == "accepted"
#     ).count()

#     earnings = db.query(func.sum(models.TeacherProfile.monthly_rate)).join(
#         models.Booking, models.Booking.teacher_id == models.TeacherProfile.user_id
#     ).filter(
#         models.Booking.teacher_id == current_user.id,
#         models.Booking.status == "accepted"
#     ).scalar() or 0

#     return {
#         "active_students": student_count,
#         "monthly_revenue": earnings,
#         "pending_requests": db.query(models.Booking).filter(
#             models.Booking.teacher_id == current_user.id, 
#             models.Booking.status == "pending"
#         ).count()
#     }

# # --- 8. DELETE AVAILABILITY SLOT ---
# @router.delete("/availability/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_availability(
#     slot_id: int,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     if current_user.role != "teacher":
#         raise HTTPException(status_code=403, detail="Unauthorized")

#     slot = db.query(models.TeacherAvailability).filter(
#         models.TeacherAvailability.id == slot_id,
#         models.TeacherAvailability.teacher_id == current_user.id
#     ).first()

#     if not slot:
#         raise HTTPException(status_code=404, detail="Slot not found or you are not the owner")

#     db.delete(slot)
#     db.commit()
#     return None 

# # --- 9. SPECIFIC PROFILE BY USER ID ---
# @router.get("/user/{u_id}", response_model=schemas.TeacherProfileOut)
# def get_profile_by_user_id(u_id: int, db: Session = Depends(get_db)):
#     result = db.query(
#         models.TeacherProfile,
#         models.User.is_verified
#     ).join(
#         models.User, models.TeacherProfile.user_id == models.User.id
#     ).filter(models.TeacherProfile.user_id == u_id).first()
    
#     if not result:
#         raise HTTPException(status_code=404, detail="Mentor Profile Not Found")

#     profile_obj, is_verified = result

#     stats = db.query(
#         func.avg(models.Review.rating).label('average'),
#         func.count(models.Review.id).label('count')
#     ).filter(models.Review.teacher_id == u_id).first()

#     p_data = schemas.TeacherProfileOut.model_validate(profile_obj)
#     p_data.is_verified = is_verified
#     p_data.average_rating = round(stats.average or 0.0, 1)
#     p_data.total_reviews = stats.count or 0
        
#     return p_data

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func 
from typing import Optional, List 
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="", tags=['Teacher Profiles'])

# --- 1. PROFILE CREATION & AUTO-UPDATE (UPSERT) ---
@router.post("", response_model=schemas.TeacherProfileOut)
def create_teacher_profile(
    profile_data: schemas.TeacherProfileCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Access Denied: Only teachers can manage professional profiles."
        )

    existing_profile_query = db.query(models.TeacherProfile).filter(
        models.TeacherProfile.user_id == current_user.id
    )
    existing_profile = existing_profile_query.first()
    
    if existing_profile:
        existing_profile_query.update(profile_data.model_dump(exclude_unset=True), synchronize_session=False)
        db.commit()
        return existing_profile_query.first()

    new_profile = models.TeacherProfile(
        user_id=current_user.id, 
        **profile_data.model_dump()
    )
    
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

# --- 11. DASHBOARD DATA FETCH ---
@router.get("/me", response_model=schemas.TeacherProfileOut)
def get_my_own_profile(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.get_current_user)
):
    profile = db.query(models.TeacherProfile).filter(
        models.TeacherProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    stats = db.query(
        func.avg(models.Review.rating).label('average'),
        func.count(models.Review.id).label('count')
    ).filter(models.Review.teacher_id == current_user.id).first()

    p_data = schemas.TeacherProfileOut.model_validate(profile)
    p_data.is_verified = current_user.is_verified
    p_data.average_rating = round(stats.average or 0.0, 1)
    p_data.total_reviews = stats.count or 0
        
    return p_data

# --- 2. DISCOVERY: UPDATED WITH ADVANCED FILTERS (CITY, EXP, RATE) ---
@router.get("/all", response_model=List[schemas.TeacherProfileOut])
def get_all_teachers(
    db: Session = Depends(get_db),
    subject: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    city: Optional[str] = None,           # 🆕 New Filter
    min_experience: Optional[int] = None  # 🆕 New Filter
):
    """
    Fetch teacher profiles with advanced filtering.
    Filters: Subject, Price Range, City, and Minimum Experience.
    """
    # Base query joining User to ensure we only show Verified mentors
    query = db.query(
        models.TeacherProfile,
        models.User.is_verified
    ).join(
        models.User, models.TeacherProfile.user_id == models.User.id
    ).filter(
        models.User.is_verified == True
    )

    # 1. Subject Filter (Case-insensitive)
    if subject:
        query = query.filter(models.TeacherProfile.subject.ilike(f"%{subject}%"))
    
    # 2. Monthly Rate Range Filters
    if min_price is not None:
        query = query.filter(models.TeacherProfile.monthly_rate >= min_price)
    if max_price is not None:
        query = query.filter(models.TeacherProfile.monthly_rate <= max_price)

    # 3. City Filter (Case-insensitive)
    if city:
        query = query.filter(models.TeacherProfile.city.ilike(f"%{city}%"))

    # 4. Experience Filter (Greater than or equal to)
    if min_experience is not None:
        query = query.filter(models.TeacherProfile.experience_years >= min_experience)

    results = query.all()
    
    final_profiles = []
    for profile_obj, is_verified in results:
        # Calculate real-time ratings for each profile in the result set
        stats = db.query(
            func.avg(models.Review.rating).label('average'),
            func.count(models.Review.id).label('count')
        ).filter(models.Review.teacher_id == profile_obj.user_id).first()
        
        p_data = schemas.TeacherProfileOut.model_validate(profile_obj)
        p_data.is_verified = is_verified
        p_data.average_rating = round(stats.average or 0.0, 1)
        p_data.total_reviews = stats.count or 0
        final_profiles.append(p_data)
        
    return final_profiles

# --- 3. TEACHER AVAILABILITY (POST) ---
@router.post("/availability", response_model=schemas.AvailabilityOut)
def set_availability(
    data: schemas.AvailabilityCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can set availability")

    existing_slot = db.query(models.TeacherAvailability).filter(
        models.TeacherAvailability.teacher_id == current_user.id,
        models.TeacherAvailability.month_year == data.month_year,
        models.TeacherAvailability.time_slot == data.time_slot
    ).first()

    if existing_slot:
        raise HTTPException(status_code=400, detail="This slot is already marked as available")

    new_slot = models.TeacherAvailability(
        teacher_id=current_user.id,
        **data.model_dump()
    )
    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)
    return new_slot

# --- 4. TEACHER AVAILABILITY (GET) ---
@router.get("/availability/{teacher_id}", response_model=List[schemas.AvailabilityOut])
def get_teacher_availability(teacher_id: int, month_year: str, db: Session = Depends(get_db)):
    slots = db.query(models.TeacherAvailability).filter(
        models.TeacherAvailability.teacher_id == teacher_id,
        models.TeacherAvailability.month_year == month_year,
        models.TeacherAvailability.is_active == True
    ).all()
    return slots

# --- 6. MANAGE BOOKINGS ---
@router.get("/bookings", response_model=List[schemas.BookingOut])
def get_incoming_requests(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can access this list")
    
    return db.query(models.Booking).filter(models.Booking.teacher_id == current_user.id).all()

@router.patch("/bookings/{booking_id}", response_model=schemas.BookingOut)
def update_hire_request(
    booking_id: int,
    status_update: schemas.BookingStatusUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    booking = db.query(models.Booking).filter(
        models.Booking.id == booking_id, 
        models.Booking.teacher_id == current_user.id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking request not found")

    booking.status = status_update.status
    db.commit()
    db.refresh(booking)
    return booking

# --- 7. TEACHER DASHBOARD STATS ---
@router.get("/dashboard/stats")
def get_teacher_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Unauthorized")

    student_count = db.query(models.Booking).filter(
        models.Booking.teacher_id == current_user.id,
        models.Booking.status == "accepted"
    ).count()

    earnings = db.query(func.sum(models.TeacherProfile.monthly_rate)).join(
        models.Booking, models.Booking.teacher_id == models.TeacherProfile.user_id
    ).filter(
        models.Booking.teacher_id == current_user.id,
        models.Booking.status == "accepted"
    ).scalar() or 0

    return {
        "active_students": student_count,
        "monthly_revenue": earnings,
        "pending_requests": db.query(models.Booking).filter(
            models.Booking.teacher_id == current_user.id, 
            models.Booking.status == "pending"
        ).count()
    }

# --- 8. DELETE AVAILABILITY SLOT ---
@router.delete("/availability/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_availability(
    slot_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Unauthorized")

    slot = db.query(models.TeacherAvailability).filter(
        models.TeacherAvailability.id == slot_id,
        models.TeacherAvailability.teacher_id == current_user.id
    ).first()

    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found or you are not the owner")

    db.delete(slot)
    db.commit()
    return None 

# --- 9. SPECIFIC PROFILE BY USER ID ---
@router.get("/user/{u_id}", response_model=schemas.TeacherProfileOut)
def get_profile_by_user_id(u_id: int, db: Session = Depends(get_db)):
    result = db.query(
        models.TeacherProfile,
        models.User.is_verified
    ).join(
        models.User, models.TeacherProfile.user_id == models.User.id
    ).filter(models.TeacherProfile.user_id == u_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Mentor Profile Not Found")

    profile_obj, is_verified = result

    stats = db.query(
        func.avg(models.Review.rating).label('average'),
        func.count(models.Review.id).label('count')
    ).filter(models.Review.teacher_id == u_id).first()

    p_data = schemas.TeacherProfileOut.model_validate(profile_obj)
    p_data.is_verified = is_verified
    p_data.average_rating = round(stats.average or 0.0, 1)
    p_data.total_reviews = stats.count or 0
        
    return p_data