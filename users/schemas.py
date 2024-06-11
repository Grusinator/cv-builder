from pydantic import BaseModel
from datetime import date
from typing import Optional


class Profile(BaseModel):
    profile_id: Optional[int] = None
    user_id: int
    full_name: Optional[str] = None
    birthdate: Optional[date] = None
    profile_picture: Optional[str] = None
    profile_description: Optional[str] = None
    email: str
    address: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    phone_number: str

    class Config:
        from_attributes = True
