from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"