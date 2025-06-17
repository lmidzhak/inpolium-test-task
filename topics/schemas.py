from typing import Optional

from pydantic import BaseModel


class TopicBase(BaseModel):
    name: str
    description: Optional[str]


class TopicCreate(TopicBase):
    pass


class Topic(TopicBase):
    id: int

    class Config:
        from_attributes = True
