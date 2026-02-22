from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter, Query, Request
from sqlalchemy.orm import Session

from core.database import get_db
from core.utilities import pagination
from user.auth import get_authenticated_user
from user.models import User

from .schemas import BlogCreateSchema, BlogResponseSchema, BlogUpdateSchema, BlogListResponseSchema
from .models import Blog, Tag


router = APIRouter(prefix="/blog", tags=["blog"])


@router.get("/blog/all", response_model=BlogListResponseSchema, 
            description="Get all blogs. This endpoint is public and does not require authentication.")
async def blog_list(
    request: Request,
    db: Session = Depends(get_db), 
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):  
    skip = (page - 1) * page_size
    total = db.query(Blog).count()
    blogs = db.query(Blog).offset(skip).limit(page_size).all()

    pagination_data = pagination(request, total, page, page_size)

    response = {**pagination_data, "data": blogs}
    return response
    

@router.get("/blog", response_model=List[BlogResponseSchema],
            description="Get blogs of the authenticated user.")
async def user_blog_list(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_authenticated_user)
):  
    blog_list = db.query(Blog).filter_by(user_id=current_user.id)
    return blog_list


@router.get("/blog/{blog_id}", response_model=BlogResponseSchema)
async def blog_detail(
    blog_id: int, db: Session = Depends(get_db), 
    current_user=Depends(get_authenticated_user)
):  
    blog_obj = db.query(Blog).filter_by(id=blog_id, user_id=current_user.id).one_or_none()
    if not blog_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found.")
    return blog_obj


@router.post("/blog", response_model=BlogResponseSchema)
async def blog_create(
    request: BlogCreateSchema, db: Session = Depends(get_db), 
    current_user=Depends(get_authenticated_user)
):
    data = request.model_dump()
    tags = data.pop("tags")
    
    # create blog obj
    blog_obj = Blog(**data)
    blog_obj.user_id = current_user.id

    # add tags to the obj
    for tag in tags:
        blog_obj.tags.append(Tag(tag_name=tag, blog_id=blog_obj.id))

    db.add(blog_obj)
    db.commit()
    db.refresh(blog_obj)
    return blog_obj


@router.put("/blog/{blog_id}", response_model=BlogResponseSchema)
async def blog_update(
    blog_id: int, request: BlogCreateSchema, db: Session = Depends(get_db), 
    current_user=Depends(get_authenticated_user)
):
    blog_obj = db.query(Blog).filter_by(id=blog_id, user_id=current_user.id).one_or_none()
    if not blog_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found.")

    for key, value in request.model_dump().items():
        setattr(blog_obj, key, value)
    db.commit()
    db.refresh(blog_obj)
    return blog_obj


@router.delete("/blog/{blog_id}")
async def blog_delete(
    blog_id: int, db: Session = Depends(get_db), 
    current_user=Depends(get_authenticated_user)
):
    blog_obj = db.query(Blog).filter_by(id=blog_id, user_id=current_user.id).one_or_none()
    if not blog_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found.")

    db.delete(blog_obj)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)