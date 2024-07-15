from datetime import date

from sqlalchemy import select

from app.bookings.dao import BookingDAO
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):

    model =  Hotels

    @classmethod
    async def get_hotels_by_location(
            cls,
            location: str,
            date_from: date,
            date_to: date
    ):

        async with async_session_maker() as session:

            query = select(Hotels).where(Hotels.location.like(f"%{location}%"))

            hotels = await session.execute(query)

            hotels = hotels.scalars().all()

            list_hotels = []

            for hotel in hotels:

                query = select(Rooms).where(Rooms.hotel_id == hotel.id)
                result = await session.execute(query)

                rooms = result.scalars().all()

                count_rooms = hotel.rooms_quantity

                for room in rooms:

                    left_rooms = await BookingDAO.get_left_rooms(
                        room_id=room.id,
                        date_from=date_from,
                        date_to=date_to,
                        session=session
                    )

                    count_rooms -= (room.quantity - left_rooms)
                if count_rooms != 0:
                    dict_hotel = hotel.as_dict()
                    dict_hotel["left_rooms"] = count_rooms
                    list_hotels.append(dict_hotel)
            return list_hotels
