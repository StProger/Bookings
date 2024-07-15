from datetime import date

from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRooms
from app.hotels.router import router


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int,
                    date_from: date,
                    date_to: date) -> list[SRooms]:

    return await RoomsDAO.get_rooms_by_hotel_id(
        hotel_id, date_from, date_to
    )
