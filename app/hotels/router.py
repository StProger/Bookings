import asyncio
from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.exceptions import BookingDifferenceDate, BookingManyDays
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel, SHotels

router = APIRouter(prefix="/hotels",
                   tags=["Отели && Комнаты"])


@router.get("/{location}")
# @cache(expire=20)
async def get_hotels_by_location(
        location: str,
        date_from: date,
        date_to: date
) -> list[SHotels]:
    print("аываы")
    if date_from >= date_to:
        raise BookingDifferenceDate

    if (date_to - date_from).days > 30:

        raise BookingManyDays

    # await asyncio.sleep(3)
    return await HotelDAO.get_hotels_by_location(location, date_from, date_to)


@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int) -> SHotel:

    return await HotelDAO.find_by_id(hotel_id)
