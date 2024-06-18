from pydantic import BaseModel

from app.hotels.models import Hotels


class SHotels(BaseModel):

    id: int
    name: str
    location: str
    services: list
    rooms_quantity: int
    image_id: int
    left_rooms: int


class SHotel(BaseModel):

    id: int
    name: str
    location: str
    services: list
    rooms_quantity: int
    image_id: int
