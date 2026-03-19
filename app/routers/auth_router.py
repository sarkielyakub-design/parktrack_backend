from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import User
from app.schemas.schema import RegisterRequest, LoginRequest
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt_handler import create_access_token

router = APIRouter()


@router.post("/register")
def register(user: RegisterRequest, db: Session = Depends(get_db)):

    new_user = User(
        email=user.email,
        password=hash_password(user.password),
        role="user"
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created"}
    

@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Wrong password")

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "role": db_user.role
    }