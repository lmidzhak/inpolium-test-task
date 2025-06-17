from datetime import datetime

from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base


class DBPost(Base):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    topic_id: Mapped[int] = mapped_column(ForeignKey('topic.id'), nullable=False)

    topic: Mapped[list["DBTopic"]] = relationship(
        'DBTopic',
        back_populates='posts'
    )
    comments: Mapped[list["DBComment"]] = relationship(
        "DBComment",
        back_populates="post",
        cascade="all, delete-orphan"
    )
