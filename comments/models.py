from datetime import datetime

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base


class DBComment(Base):
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    post: Mapped["DBPost"] = relationship(
        "DBPost", back_populates="comments"
    )
