from datetime import date

from fastapi import APIRouter

from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotels, SHotel

router = APIRouter(prefix="/hotels",
                   tags=["Отели && Комнаты"])


@router.get("/{location}")
async def get_hotels(
        location: str,
        date_from: date,
        date_to: date
) -> list[SHotels]:

    return await HotelDAO.get_hotels_by_location(location, date_from, date_to)


@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int) -> SHotel:

    return await HotelDAO.find_by_id(hotel_id)
