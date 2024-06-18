from datetime import date

from sqlalchemy import select, and_, or_, func, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class BookingDAO(BaseDAO):

    model = Bookings

    @classmethod
    async def delete_(cls, booking_id: int):

        async with async_session_maker() as session:

            query = delete(Bookings).where(Bookings.id == booking_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def get_left_rooms(cls,
                             room_id: int,
                             date_from: date,
                             date_to: date,
                             session: AsyncSession):

        booking_rooms = select(Bookings).where(
            and_(
                Bookings.room_id == room_id,
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_to
                    )
                )
            )
        ).cte("booked_rooms")

        left_rooms = select(
            (Rooms.quantity - func.count(booking_rooms.c.room_id)).label("left_rooms")
        ).select_from(Rooms).join(
            booking_rooms, booking_rooms.c.room_id == Rooms.id, isouter=True
        ).where(
            Rooms.id == room_id
        ).group_by(Rooms.quantity)

        result = await session.execute(left_rooms)
        rooms_left: int = result.scalar()

        return rooms_left

    @classmethod
    async def add(cls,
                  user_id: int,
                  room_id: int,
                  date_from: date,
                  date_to: date):

        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            (
                date_from >= '2023-05-15' AND date_from <= '2023-06-20'
            ) OR
            (
                date_from <= '2023-05-15' AND date_to > '2023-05-15'
            )
        )

        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity;

"""
        async with async_session_maker() as session:
            booking_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_to
                        )
                    )
                )
            ).cte("booked_rooms")


            left_rooms = select(
                (Rooms.quantity - func.count(booking_rooms.c.room_id)).label("left_rooms")
            ).select_from(Rooms).join(
                booking_rooms, booking_rooms.c.room_id == Rooms.id, isouter=True
            ).where(
                Rooms.id == room_id
            ).group_by(Rooms.quantity)


            result = await session.execute(left_rooms)
            rooms_left: int = result.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price = price.scalar()
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(Bookings)
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()

            else:

                return None

    @classmethod
    async def find_all_bookings(
            cls,
            user_id: int
    ):

        async with async_session_maker() as session:

            """
                        WITH user_bookings AS (
                SELECT * FROM bookings
                WHERE user_id = 3
            )
            
            SELECT rooms.image_id, rooms.name, rooms.description, rooms.services, user_bookings.* FROM rooms
            LEFT JOIN user_bookings ON user_bookings.room_id = rooms.id
            WHERE user_bookings.user_id = 3;
            """

            user_bookings = select(Bookings).where(Bookings.user_id == user_id).cte("user_bookings")

            query = select(
                Rooms.image_id,
                Rooms.name,
                Rooms.description,
                Rooms.services,
                user_bookings.columns
            ).select_from(Rooms).join(
                user_bookings,
                user_bookings.c.room_id == Rooms.id,
                isouter=True
            ).where(
                user_bookings.c.user_id == user_id
            )

            result = await session.execute(query)

            return result.mappings().all()
