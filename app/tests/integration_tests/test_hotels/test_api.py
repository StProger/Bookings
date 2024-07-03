import pytest
from httpx import AsyncClient

from app.bookings.dao import BookingDAO


async def test_get_bookings_user(authenticated_ac: AsyncClient):

    response = await authenticated_ac.get("/bookings")
    print(response.json())

    assert len(response.json()) != 0

    for booking in response.json():

        await BookingDAO.delete_(booking["id"])

    response = await authenticated_ac.get("/bookings")

    assert len(response.json()) == 0