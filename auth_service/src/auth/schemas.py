from typing import Any, Self

from pydantic import BaseModel, Field, EmailStr, model_validator

from auth_service.src.auth.exceptions import LoginValidateException, RegisterValidateException


class UserSchemas(BaseModel):
    id: int = Field(None)
    username: str = Field(None, min_length=6, max_length=24)
    email: EmailStr = Field(None)
    password: str = Field(None, min_length=8, max_length=22)
    first_name: str = Field(None)
    surname: str = Field(None)

    @model_validator(mode="before")
    def validate(self, value: Any) -> Self:

        if value.get('is_login'):
            if not value.get("username") or not value.get("password"):
                raise LoginValidateException()

        elif value.get('is_register'):
            if not value.get("username") or not value.get("password") or not value.get("email"):
                raise RegisterValidateException()

        return value
