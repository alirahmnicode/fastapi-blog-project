import random
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from slugify import slugify

from user.models import UserModel
from blog.models import BlogModel, TagModel
from core.database import DATABASE_URL

# ---- Setup DB connection ----
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

fake = Faker()


def seed_user(db):
    # Ensure at least one user exists
    user = session.query(UserModel).first()
    if not user:
        user = UserModel(
            username=fake.user_name(), email=fake.email(), password="hashedpassword"
        )
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def seed_blogs(db, user, count=10):
    for _ in range(count):
        title = fake.sentence(nb_words=6)
        slug = slugify(title) + f"-{random.randint(1000, 9999)}"

        is_published = random.choice([True, False])
        published_at = (
            datetime.now(timezone.utc) if is_published else None
        )

        blog = BlogModel(
            title=title,
            slug=slug,
            content=fake.text(max_nb_chars=1000),
            excerpt=fake.text(max_nb_chars=200),
            image_url=f"https://picsum.photos/seed/{random.randint(1, 1000)}/800/400",
            is_published=is_published,
            published_at=published_at,
            user_id=user.id,
        )

        # Add 1–5 random tags per blog
        for _ in range(random.randint(1, 5)):
            tag = TagModel(tag_name=fake.word())
            blog.tags.append(tag)

        db.add(blog)

    db.commit()
    print(f"✅ Successfully inserted {count} fake blogs with tags!")


def main():
    db = SessionLocal()
    try:
        user = seed_user(db)
        seed_blogs(db, user)
    finally:
        db.close()


if __name__ == "__main__":
    main()
