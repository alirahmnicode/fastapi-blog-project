from typing import List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class TagBaseSchema(BaseModel):
    tag_name: str


class TagCreateSchema(TagBaseSchema):
    pass


class TagResponseSchema(TagBaseSchema):
    id: int


class BlogBaseSchema(BaseModel):
    title: str = Field(
        ..., min_length=3, max_length=255, description="title of the blog post."
    )
    description: str = Field(
        ..., min_length=3, description="description of the blog post."
    )
    created_at: datetime
    updated_at: datetime


class BlogResponseSchema(BlogBaseSchema):
    id: int
    user_id: int = Field(..., description="id of the user.")
    tags: List[TagResponseSchema]


class BlogListResponseSchema(BaseModel):
    total: int
    page: int
    page_size: int
    next: str | None = None
    previous: str | None = None
    data: List[BlogResponseSchema]


class BlogCreateSchema(BlogBaseSchema):
    tags: List[str] = []


class BlogUpdateSchema(BlogBaseSchema):
    pass
