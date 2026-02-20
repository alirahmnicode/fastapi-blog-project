from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register")
async def register_user():
    return {"message": "User registration endpoint"}


@router.post("/login")
async def login_user():
    return {"message": "User login endpoint"}