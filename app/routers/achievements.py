# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List
# from .. import models, schemas, oauth2
# from ..database import get_db

# router = APIRouter(prefix="", tags=['Hall of Fame'])

# # --- 1. ADMIN ONLY: Add a Success Story ---
# @router.post("", response_model=schemas.AchievementOut, status_code=status.HTTP_201_CREATED)
# def add_achievement(
#     data: schemas.AchievementCreate, 
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     # 1. Security Check
#     if current_user.role != "admin":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, 
#             detail="Only admins can update the Success Wall"
#         )

#     # 2. Verify Teacher Exists
#     # We fetch the teacher early to get their name and prevent 500 errors
#     teacher = db.query(models.User).filter(models.User.id == data.teacher_id).first()
#     if not teacher:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, 
#             detail=f"Teacher with ID {data.teacher_id} not found"
#         )

#     # 3. Create Achievement
#     new_achievement = models.Achievement(**data.model_dump())
    
#     db.add(new_achievement)
#     db.commit()
#     db.refresh(new_achievement)
    
#     # 4. Critical Step: Attach the teacher_name for the Schema
#     # We use setattr to bypass SQLAlchemy's strict column checking
#     setattr(new_achievement, "teacher_name", teacher.full_name if hasattr(teacher, 'full_name') else teacher.email)
    
#     return new_achievement

# # --- 2. PUBLIC: Fetch for SuccessWall Component ---
# @router.get("", response_model=List[schemas.AchievementOut])
# def get_hall_of_fame(db: Session = Depends(get_db)):
#     """Fetch featured success stories for the landing page."""
    
#     # Query achievements and join the teacher (User) to avoid N+1 query issues
#     achievements = db.query(models.Achievement).filter(
#         models.Achievement.is_featured == True
#     ).all()
    
#     for a in achievements:
#         # Dynamically add teacher_name so AchievementOut can find it
#         if a.teacher:
#             # Check if your User model uses 'full_name' or 'name'
#             a.teacher_name = getattr(a.teacher, 'full_name', a.teacher.email)
#         else:
#             a.teacher_name = "Verified Tutor"
        
#     return achievements

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="", tags=['Hall of Fame'])

# --- 1. ADMIN ONLY: Add a Success Story ---
@router.post("", response_model=schemas.AchievementOut, status_code=status.HTTP_201_CREATED)
def add_achievement(
    data: schemas.AchievementCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    # 1. Security Check
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Only admins can update the Success Wall"
        )

    # 2. Verify Teacher Exists (Fetch from TeacherProfile to get the real name)
    teacher_profile = db.query(models.TeacherProfile).filter(models.TeacherProfile.user_id == data.teacher_id).first()
    
    if not teacher_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Teacher Profile with User ID {data.teacher_id} not found."
        )

    # 3. Create Achievement
    new_achievement = models.Achievement(**data.model_dump())
    
    db.add(new_achievement)
    db.commit()
    db.refresh(new_achievement)
    
    # 4. Attach name for the Schema response
    setattr(new_achievement, "teacher_name", teacher_profile.full_name)
    
    return new_achievement

# --- 2. PUBLIC/ADMIN: Fetch all for Slider & Management ---
@router.get("", response_model=List[schemas.AchievementOut])
def get_hall_of_fame(db: Session = Depends(get_db)):
    """Fetch success stories. Used by both Landing Page and Admin Dashboard."""
    
    # We fetch all achievements. If you want to limit the landing page later, 
    # you can add a .filter(models.Achievement.is_featured == True)
    achievements = db.query(models.Achievement).all()
    
    for a in achievements:
        # Join logic to pull the teacher's name from TeacherProfile
        teacher = db.query(models.TeacherProfile).filter(models.TeacherProfile.user_id == a.teacher_id).first()
        if teacher:
            a.teacher_name = teacher.full_name
        else:
            a.teacher_name = "Adhya Mentor"
            
    return achievements

# --- 3. ADMIN ONLY: Delete an Achievement (NEW) ---
@router.delete("/{achievement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_achievement(
    achievement_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Allows Admin to remove a story from the Success Wall."""
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")

    achievement = db.query(models.Achievement).filter(models.Achievement.id == achievement_id).first()
    
    if not achievement:
        raise HTTPException(status_code=404, detail="Achievement not found")

    db.delete(achievement)
    db.commit()
    return None