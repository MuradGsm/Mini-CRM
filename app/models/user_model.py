from app.core.database import Base, int_pk
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

class User(Base):
    id: Mapped[int_pk]
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    clients: Mapped[List['Client']] = relationship(back_populates='user')

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"