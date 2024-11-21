from pydantic import BaseModel, Field, EmailStr


class UserSchemas(BaseModel):
    id: int | None = Field(None)
    username: str | None  = Field(None, min_length=6, max_length=24)
    email: EmailStr | None  = Field(None)
    password: str | None  = Field(None, min_length=8)
    first_name: str | None  = Field(None)
    surname: str | None  = Field(None)


class TokenSchemas(BaseModel):
    access_token: str | None = Field(None)
    refresh_token: str | None = Field(None)


class ValidResponseSchemas(BaseModel):
    valid: bool
    message: str
