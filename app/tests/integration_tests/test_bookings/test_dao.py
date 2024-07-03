from datetime import datetime

import pytest
from httpx import AsyncClient

from app.bookings.dao import BookingDAO


@pytest.mark.parametrize("user_id, room_id, date_from, date_to", [
    (2, 2, "2023-07-10", "2023-07-24"),
])
async def test_add_and_get_booking(
    user_id,
    room_id,
    date_from,
    date_to
):

    new_booking = await BookingDAO.add(
        user_id=user_id,
        room_id=room_id,
        date_from=datetime.strptime(date_from, "%Y-%m-%d"),
        date_to=datetime.strptime(date_to, "%Y-%m-%d")
    )

    assert new_booking.user_id == user_id
    assert new_booking.room_id == room_id

    new_booking = await BookingDAO.find_by_id(new_booking.id)

    assert new_booking is not None


async def test_add_read_delete_booking(authenticated_ac: AsyncClient):

    new_booking = await BookingDAO.add(
        user_id=1,
        room_id=2,
        date_from=datetime.strptime("2024-05-15", "%Y-%m-%d"),
        date_to=datetime.strptime("2024-05-25", "%Y-%m-%d")
    )

    booking = await BookingDAO.find_by_id(new_booking.id)

    assert booking is not None

    await BookingDAO.delete_(booking.id)

    booking = await BookingDAO.find_by_id(new_booking.id)

    assert booking is None
