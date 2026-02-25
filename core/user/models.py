from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from core.database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class UserModel(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    blogs = relationship("BlogModel", back_populates="user",
                         cascade="all, delete-orphan")

    def hash_password(self, plain_password: str):
        "Hash the password using a secure hashing algorithm (bcrypt)."
        print(pwd_context.verify(plain_password, pwd_context.hash(plain_password)))
        return pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        "Verify the provided password against the stored hashed password."
        return pwd_context.verify(plain_password, self.password)

    def set_password(self, plain_password: str):
        "Set the user's password by hashing it before storing."
        self.password = self.hash_password(plain_password)
