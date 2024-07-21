from datetime import date

from fastapi import APIRouter, Depends
from fastapi_versioning import version
from pydantic import parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SBookings
from app.exceptions import (BookingDifferenceDate, BookingManyDays,
                            RoomCannotBeBooked)
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
@version(1)
async def get_bookings(user: Users = Depends(get_current_user)):

    return await BookingDAO.find_all_bookings(user.id)


@router.delete("/{booking_id}")
@version(1)
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):

    await BookingDAO.delete_(booking_id)


@router.post("")
@version(1)
async def add_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: Users = Depends(get_current_user)
):
    if date_from >= date_to:
        raise BookingDifferenceDate

    if (date_to - date_from).days > 30:

        raise BookingManyDays

    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)

    # booking_dict = parse_obj_as(SBooking, booking).dict()
    # send_booking_confirmation_email.delay(booking_dict, user.email)
    if not booking:

        raise RoomCannotBeBooked
    else:

        return booking
