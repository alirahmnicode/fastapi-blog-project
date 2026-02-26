from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
    ForeignKey,
    Boolean,
    Table,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from slugify import slugify
from core.database import Base

blog_likes = Table(
    "blog_likes",
    Base.metadata,
    Column(
        "user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "blog_id", Integer, ForeignKey("blogs.id", ondelete="CASCADE"), primary_key=True
    ),
)


class BlogModel(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    content = Column(String)
    excerpt = Column(String)
    image_url = Column(String)
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime(timezone=True))
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("UserModel", back_populates="blogs")

    tags = relationship("TagModel", back_populates="blog", cascade="all, delete-orphan")
    liked_by_users: Mapped[list["UserModel"]] = relationship(
        secondary=blog_likes, back_populates="liked_blogs"
    )

    def set_slug(self):
        self.slug = slugify(self.title) + f"-{self.id}"

    def set_published_date(self):
        if self.is_published and not self.published_at:
            self.published_at = func.now()
        else:
            self.published_at = None


class TagModel(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String, index=True)
    blog_id = Column(
        Integer, ForeignKey("blogs.id", ondelete="CASCADE"), nullable=False
    )

    blog = relationship("BlogModel", back_populates="tags")
