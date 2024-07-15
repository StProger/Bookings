from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.dao import BookingDAO
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class RoomsDAO(BaseDAO):

    model = Rooms

    @classmethod
    async def get_rooms_by_hotel_id(
            cls,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):

        async with async_session_maker() as session:

            session: AsyncSession
            query = select(Rooms).where(Rooms.hotel_id == hotel_id)

            result = await session.execute(query)

            rooms = result.scalars().all()

            list_rooms = []

            for room in rooms:

                room: Rooms

                count_rooms = room.quantity

                count_rooms -= await BookingDAO.get_left_rooms(
                    room_id=room.id,
                    date_from=date_from,
                    date_to=date_to,
                    session=session
                )

                total_price = (date_to - date_from).days * room.price

                json_room = room.as_dict()

                del json_room["quantity"]

                json_room["left_rooms"] = count_rooms
                json_room["total_cost"] = total_price

                list_rooms.append(json_room)

            return list_rooms
