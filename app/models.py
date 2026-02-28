from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    # This prevents "Table already defined" errors if the table exists in PostgreSQL
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    
    # CHANGED: Using 'password' to match your auth.py and registration logic
    password = Column(String, nullable=False) 
    
    role = Column(String, default="student")
    is_verified = Column(Boolean, default=False)
   
    interview_status = Column(String, server_default='pending', nullable=False)
    # Automatically captures the timestamp when a user registers
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to connect with TeacherProfile (1-to-1 mapping)
    profile = relationship("TeacherProfile", back_populates="owner", uselist=False)


class TeacherProfile(Base):
    __tablename__ = "teacher_profiles"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    
    # Link to the User table with CASCADE delete
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    
    # Profile Information
    full_name = Column(String, nullable=False)
    subject = Column(String, nullable=False) 
    bio = Column(Text, nullable=True)
    experience_years = Column(Integer, default=0)
    
    # Financials - Matches your pgAdmin screenshot
    monthly_rate = Column(Integer, nullable=False) 
    
    # Media and Location
    profile_picture = Column(String, nullable=True)
    city = Column(String(100), nullable=True) 

    # Link back to the User object
    owner = relationship("User", back_populates="profile")

class StudentProfile(Base):
    __tablename__ = "student_profiles"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    
    # The 4 fields you requested
    full_name = Column(String, nullable=False)
    grade_class = Column(String, nullable=False) # e.g., "10th Standard" or "B.Tech"
    city = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)

    # Relationship back to the User
    owner = relationship("User", backref="student_profile")


class TeacherAvailability(Base):
    __tablename__ = "teacher_availability"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    month_year = Column(String, nullable=False) # e.g., "March 2026"
    time_slot = Column(String, nullable=False)  # e.g., "14:00 - 16:00"
    is_active = Column(Boolean, default=True)   # Teacher can toggle this off

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    subject = Column(String, nullable=False)
    
    # Monthly Block Logic
    month_year = Column(String, nullable=False) # e.g., "March 2026"
    time_slot = Column(String, nullable=False)  # e.g., "14:00 - 16:00"
    
    status = Column(String, default="pending") 
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    
    rating = Column(Integer, nullable=False)  # 1–5
    comment = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    student = relationship("User", foreign_keys=[student_id])
    booking = relationship("Booking")


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, nullable=False)
    score = Column(String, nullable=False)        # e.g., "98%", "AIR 500"
    subject = Column(String, nullable=False)      # The subject they excelled in
    detail = Column(String, nullable=True)       # e.g., "CBSE Board Exams"
    
    # Link to the teacher who guided them
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # UI Customization (so Admin can choose the card color in React)
    color_theme = Column(String, default="bg-blue-50") 
    
    is_featured = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to get the Teacher's name automatically
    teacher = relationship("User")