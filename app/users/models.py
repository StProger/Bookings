from app.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON


class Users(Base):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)