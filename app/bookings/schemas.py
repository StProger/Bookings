from datetime import date

from pydantic import BaseModel

class SBooking(BaseModel):

    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    class Config:

        from_attributes = True


class SBookings(BaseModel):

    room_id: int
    user_id: int
    date_from: date
    date_to: date
    booking_id: int
    price: int
    total_cost: int
    total_days: int
    name: str
    description: str | None
    services: list
    image_id: int