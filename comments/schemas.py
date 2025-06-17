from datetime import datetime

from pydantic import BaseModel


class CommentBase(BaseModel):
    text: str
    post_id: int

    class Config:
        from_attributes = True


class CommentCreate(CommentBase):
    created_at: datetime


class CommentUpdate(CommentBase):
    updated_at: datetime


class Comment(CommentBase):
    id: int
