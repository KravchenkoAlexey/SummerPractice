from sqlalchemy import Column, Integer, String, Text, Boolean, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped

from app.service.db.base import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    title: Mapped[str] = Column(String, index=True)
    description: Mapped[str] = Column(Text)
    media_uri: Mapped[str] = Column(String)
    approved: Mapped[bool] = Column(Boolean, default=False)
    user: Mapped['User'] = Column(BigInteger, ForeignKey('users.id'))
    likes_count: Mapped[int] = Column(Integer, default=0)
    dislikes_count: Mapped[int] = Column(Integer, default=0)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(BigInteger, primary_key=True, index=True)
    is_admin: Mapped[bool] = Column(Boolean, default=False)

