from sqlalchemy import  Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class DBTopic(Base):
    __tablename__ = 'topic'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description = mapped_column(String(255), nullable=True)

    posts: Mapped[list["DBPost"]] = relationship(
         "DBPost", back_populates="topic", cascade="all, delete-orphan"
    )
