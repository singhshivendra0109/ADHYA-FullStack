from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, models, utils, schemas

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    # 1. Fetch user by email (username field in OAuth2 form)
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Invalid Credentials"
        )

    # 2. Verify the password
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Invalid Credentials"
        )

    # 3. Create the JWT Token
    access_token = utils.create_access_token(data={"user_id": user.id, "role": user.role})

    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "role": user.role
    }