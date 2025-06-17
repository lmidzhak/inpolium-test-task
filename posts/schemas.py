from datetime import datetime

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    topic_id: int

    class Config:
        from_attributes = True


class PostCreate(PostBase):
    created_at: datetime


class PostUpdate(PostBase):
    updated_at: datetime


class Post(PostBase):
    id: int
