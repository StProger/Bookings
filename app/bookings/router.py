from datetime import date

from fastapi import APIRouter, Depends

from app.bookings.dao import BookingDAO
from app.users.models import Users
from app.users.dependencies import get_current_user
from app.exceptions import RoomCannotBeBooked
from app.bookings.schemas import SBookings


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookings]:

    return await BookingDAO.find_all_bookings(user.id)


@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):

    await BookingDAO.delete_(booking_id)


@router.post("")
async def add_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: Users = Depends(get_current_user)
):
    print(user)
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:

        raise RoomCannotBeBooked
    else:

        return booking
