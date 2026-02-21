from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from core.database import Base, engine
from core.blog.routes import router as blog_router
from core.user.router import router as user_router


app = FastAPI()

app.include_router(blog_router)
app.include_router(user_router)