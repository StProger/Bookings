from pydantic import BaseModel


class SRooms(BaseModel):

    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list
    image_id: int
    left_rooms: int
    total_cost: int