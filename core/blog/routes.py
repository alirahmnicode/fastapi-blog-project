from typing import List
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    Response,
    APIRouter,
    Query,
    Request,
)
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from core.database import get_db
from core.utilities import pagination
from user.auth import get_authenticated_user
from user.models import UserModel

from .schemas import (
    BlogCreateSchema,
    BlogResponseSchema,
    BlogUpdateSchema,
    BlogListResponseSchema,
)
from .models import BlogModel, TagModel

router = APIRouter(prefix="/blogs", tags=["blog"])


@router.get(
    "/all",
    response_model=BlogListResponseSchema,
    description="Get all blogs. This endpoint is public and does not require authentication.",
)
async def blog_list(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    skip = (page - 1) * page_size
    total = db.query(BlogModel).count()
    blogs = db.query(BlogModel).offset(skip).limit(page_size).all()

    pagination_data = pagination(request, total, page, page_size)

    response = {**pagination_data, "data": blogs}
    return response


@router.get(
    "/",
    response_model=List[BlogResponseSchema],
    description="Get blogs of the authenticated user.",
)
async def user_blog_list(
    db: Session = Depends(get_db), current_user: UserModel = Depends(get_authenticated_user)
):
    blog_list = db.query(BlogModel).filter_by(user_id=current_user.id)
    return blog_list


@router.get("/{blog_id}", response_model=BlogResponseSchema)
async def blog_detail(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_authenticated_user),
):
    blog_obj = (
        db.query(BlogModel).filter_by(
            id=blog_id, user_id=current_user.id).one_or_none()
    )
    if not blog_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found."
        )
    return blog_obj


@router.post("/", response_model=BlogResponseSchema)
async def blog_create(
    request: BlogCreateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_authenticated_user),
):
    data = request.model_dump()
    tags = data.pop("tags")
    slug = data.pop("slug")
    is_published = data.pop("is_published")

    # create blog obj
    blog_obj = BlogModel(**data)
    blog_obj.user_id = current_user.id
    blog_obj.set_slug()
    # add tags to the obj
    for tag in tags:
        blog_obj.tags.append(TagModel(tag_name=tag, blog_id=blog_obj.id))

    db.add(blog_obj)
    db.commit()
    db.refresh(blog_obj)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(blog_obj))


@router.put("/{blog_id}", response_model=BlogResponseSchema)
async def blog_update(
    blog_id: int,
    request: BlogCreateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_authenticated_user),
):
    blog_obj = (
        db.query(BlogModel).filter_by(
            id=blog_id, user_id=current_user.id).one_or_none()
    )
    if not blog_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found."
        )

    for key, value in request.model_dump().items():
        setattr(blog_obj, key, value)
    db.commit()
    db.refresh(blog_obj)
    return blog_obj


@router.delete("/{blog_id}")
async def blog_delete(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_authenticated_user),
):
    blog_obj = (
        db.query(BlogModel).filter_by(
            id=blog_id, user_id=current_user.id).one_or_none()
    )
    if not blog_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found."
        )

    db.delete(blog_obj)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
