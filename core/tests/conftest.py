import random
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
import pytest
from main import app
from core.database import Base, engine, create_engine, sessionmaker, get_db
from user.auth import generate_access_token
from user.models import UserModel
from blog.models import BlogModel, TagModel
from faker import Faker
from slugify import slugify

fake = Faker()

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="package")
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module", autouse=True)
def override_dependencies(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture(scope="session", autouse=True)
def tear_up_and_down_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="package")
def anon_client(db_session):
    return TestClient(app)


@pytest.fixture(scope="package")
def auth_client(db_session):
    client = TestClient(app)
    user = db_session.query(UserModel).filter_by(username="testuser").one()
    access_token = generate_access_token(user.id)
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    yield client


@pytest.fixture(scope="package", autouse=True)
def generate_mock_data(db_session):
    # create a user
    user = UserModel(username="testuser", email="testuser@example.com")
    user.set_password("12345678")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    for _ in range(10):
        title = fake.sentence(nb_words=6)
        slug = slugify(title) + f"-{random.randint(1000, 9999)}"

        is_published = random.choice([True, False])
        published_at = datetime.now(timezone.utc) if is_published else None

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

        db_session.add(blog)

    db_session.commit()


@pytest.fixture(scope="function")
def random_blog(db_session):
    user = db_session.query(UserModel).filter_by(username="testuser").first()
    blog = db_session.query(BlogModel).filter_by(user_id=user.id).first()
    return blog


@pytest.fixture(scope="function")
def fake_blog_data():
    return {
        "title": "new blog",
        "slug": slugify("new blog") + f"-{random.randint(1000, 9999)}",
        "content": "content of the new blog",
        "excerpt": "excerpt of the new blog",
        "image_url": f"https://picsum.photos/seed/{random.randint(1, 1000)}/800/400",
        "is_published": True,
        "published_at": datetime.now(timezone.utc).isoformat(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "tags": [fake.word() for _ in range(random.randint(1, 5))],
    }
