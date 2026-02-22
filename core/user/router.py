from fastapi import APIRouter, Depends, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from core.database import get_db
from sqlalchemy.orm import Session

from .schemas import UserCreateSchema, UserLoginSchema, UserResponseSchema
from .models import User
from .auth import (
    generate_access_token,
    generate_refresh_token,
    decode_refresh_token,
)


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register")
async def register_user(request: UserCreateSchema, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(
        (User.username == request.username) | (User.email == request.email)
    ).first()

    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already exists!")

    user = User(username=request.username, email=request.email)
    user.set_password(request.password)
    db.add(user)
    db.commit()
    return {"message": "User registered successfully", "user": user}


@router.post("/login")
async def login_user(request: UserLoginSchema, db: Session = Depends(get_db)):
    user_obj = (
        db.query(User)
        .filter_by(username=request.username.lower())
        .first()
    )

    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user or password",
        )
    if not user_obj.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user or password",
        )
    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)
    return JSONResponse(
        content={
            "detail": "logged in successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )