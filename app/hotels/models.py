from app.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON


class Hotels(Base):

    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    services: Mapped[dict] = mapped_column(JSON, nullable=False)
    rooms_quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]

    room = relationship("Rooms", back_populates="hotel")

    def __str__(self):

        return f"Отель {self.name} {self.location[:30]}"