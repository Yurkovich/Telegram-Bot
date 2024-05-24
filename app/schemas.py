
from pydantic import BaseModel, Field, field_validator
import re

class UserCreate(BaseModel):
    username: str = Field(..., min_length=7)
    password: str = Field(..., min_length=8)

    @field_validator("username")
    def validate_username(cls, v):
        if not re.match(r'^[A-Za-z0-9_]+$', v):
            raise ValueError("Логин может содержать только буквы латинского алфавита, цифры и символ подчеркивания.")
        if v.startswith('_'):
            raise ValueError("Логин не должен начинаться с символа подчеркивания.")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if not re.match(r'^[A-Za-z0-9_]+$', v):
            raise ValueError("Пароль может содержать только буквы латинского алфавита, цифры и символ подчеркивания.")
        return v