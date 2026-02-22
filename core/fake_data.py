from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random

from user.models import User
from blog.models import Blog, Tag
from core.database import DATABASE_URL

# ---- Setup DB connection ----
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

fake = Faker()

def seed_data():
    # Ensure at least one user exists
    user = session.query(User).first()
    if not user:
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password="hashedpassword"
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    for _ in range(10):
        blog = Blog(
            title=fake.sentence(nb_words=6),
            description=fake.text(max_nb_chars=200),
            user_id=user.id
        )

        # Add 1–5 random tags per blog
        for _ in range(random.randint(1, 5)):
            tag = Tag(tag_name=fake.word())
            blog.tags.append(tag)

        session.add(blog)

    session.commit()
    print("✅ Successfully inserted 10 fake blogs with tags!")

if __name__ == "__main__":
    seed_data()
    session.close()