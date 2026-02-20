from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    password: str


class UserLoginSchema(UserBaseSchema):
    password: str
    
    
class UserResponseSchema(UserBaseSchema):
    id: int
