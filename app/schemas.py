from pydantic import BaseModel
from datetime import datetime


class LinkCreate(BaseModel):

    original_url: str
    custom_alias: str | None = None
    expires_at: datetime | None = None


class LinkResponse(BaseModel):

    short_url: str


class LinkStats(BaseModel):

    original_url: str
    created_at: datetime
    click_count: int
    last_used_at: datetime | None


class UserCreate(BaseModel):

    email: str
    password: str


class UserLogin(BaseModel):

    email: str
    password: str
