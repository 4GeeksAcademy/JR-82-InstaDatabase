from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    posts: Mapped[List["Post"]] = relationship(back_populates="author")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "username": self.username
            # do not serialize the password, its a security breach
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    username: Mapped[str] = mapped_column(nullable=False)
    author: Mapped["User"] = relationship(back_populates="posts")
    medias: Mapped[List["Media"]] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "user_id": self.user_id
            # do not serialize the password, its a security breach
        }


class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_to_id: Mapped[str] = mapped_column(nullable=False)
    author: Mapped["User"] = relationship(back_populates="follower")

    def serialize(self):
        return {
            "id": self.id,
            "user_to_id": self.user_to_id,
            "user_from_id": self.user_from_id
            # do not serialize the password, its a security breach
        }


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(
        Enum('image', 'video', name='media_types'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    url: Mapped["str"] = mapped_column(nullable=False, unique=True)
    posts: Mapped["Post"] = relationship(back_populates="posts")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
            # do not serialize the password, its a security breach
        }
