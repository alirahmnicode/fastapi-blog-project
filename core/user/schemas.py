from pydantic import BaseModel, EmailStr, field_validator, Field


class UserBaseSchema(BaseModel):
    username: str


class UserCreateSchema(UserBaseSchema):
    email: EmailStr
    password: str = Field(..., min_length=8)
    password_confirm: str = Field(..., min_length=8)

    @field_validator("password_confirm")
    def passwords_match(cls, value, values):
        if value != values.data.get("password"):
            raise ValueError("Passwords do not match!")
        return value


class UserLoginSchema(UserBaseSchema):
    password: str


class UserResponseSchema(UserBaseSchema):
    id: int


class UserRefreshTokenSchema(BaseModel):
    token: str = Field(...)
