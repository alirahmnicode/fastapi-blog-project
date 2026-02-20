from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session
from .schemas import BlogCreateSchema, BlogResponseSchema, BlogUpdateSchema
from core.database import get_db
from .models import Blog, Tag


router = APIRouter(prefix="/blog", tags=["blog"])

@router.get("/blog", response_model=List[BlogResponseSchema])
async def blog_list(db: Session = Depends(get_db)):
    blog_list = db.query(Blog).all()
    return blog_list


@router.get("/blog/{blog_id}", response_model=BlogResponseSchema)
async def blog_detail(blog_id: int, db: Session = Depends(get_db)):
    blog_obj = db.query(Blog).filter_by(id=blog_id).one_or_none()
    if not blog_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found.")
    return blog_obj


@router.post("/blog", response_model=BlogResponseSchema)
async def blog_create(request: BlogCreateSchema, db: Session = Depends(get_db)):
    data = request.model_dump()
    tags = data.pop("tags")
    
    # create blog obj
    blog_obj = Blog(**data)

    # add tags to the obj
    for tag in tags:
        blog_obj.tags.routerend(Tag(tag_name=tag, blog_id=blog_obj.id))

    db.add(blog_obj)
    db.commit()
    db.refresh(blog_obj)
    return blog_obj


@router.put("/blog/{blog_id}", response_model=BlogResponseSchema)
async def blog_update(blog_id: int, request: BlogCreateSchema, db: Session = Depends(get_db)):
    blog_obj = db.get(Blog, blog_id)
    if not blog_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found.")

    for key, value in request.model_dump().items():
        setattr(blog_obj, key, value)
    db.commit()
    db.refresh(blog_obj)
    return blog_obj


@router.delete("/blog/{blog_id}")
async def blog_delete(blog_id: int, db: Session = Depends(get_db)):
    blog_obj = db.get(Blog, blog_id)
    if not blog_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found.")

    db.delete(blog_obj)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)