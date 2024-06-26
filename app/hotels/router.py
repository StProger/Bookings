import asyncio
from datetime import date

from fastapi import APIRouter

from fastapi_cache.decorator import cache

from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotels, SHotel

router = APIRouter(prefix="/hotels",
                   tags=["Отели && Комнаты"])


@router.get("/{location}")
@cache(expire=20)
async def get_hotels_by_location(
        location: str,
        date_from: date,
        date_to: date
) -> list[SHotels]:
    await asyncio.sleep(3)
    return await HotelDAO.get_hotels_by_location(location, date_from, date_to)


@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int) -> SHotel:

    return await HotelDAO.find_by_id(hotel_id)
