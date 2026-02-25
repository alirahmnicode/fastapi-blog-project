from typing import List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


#      = Column(Boolean, default=False)
#      = Column(DateTime(timezone=True))
#     created_at = Column(
#         DateTime(timezone=True), server_default=func.now(), nullable=False
#     )
#     updated_at = Column(
#         DateTime(timezone=True),
#         server_default=func.now(),
#         onupdate=func.now(),
#         nullable=False,
#     )

#     user_id = Column(
#         Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
#     )
#     user = relationship("UserModel", back_populates="blogs")

#     tags = relationship("TagModel", back_populates="blog",
#                         cascade="all, delete-orphan")

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
    slug: str = Field(..., min_length=3, max_length=255,
                      description="slug of the blog post.")
    content: str = Field(
        ..., min_length=3, description="content of the blog post."
    )
    excerpt: str = Field(
        ..., min_length=3, max_length=500, description="excerpt of the blog post."
    )
    image_url: str | None = Field(default=None)
    is_published: bool = Field(default=False)
    published_at: datetime | None = Field(default=None)
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
