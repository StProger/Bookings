import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("location, date_from, date_to, status_code", [
    ("Алтай", "2023-01-16", "2023-01-10", 400),
    ("Алтай", "2023-01-10", "2023-02-25", 400),
    ("Алтай", "2023-01-10", "2023-01-25", 200)
])
async def test_get_hotels_by_location(ac: AsyncClient, location, date_from, date_to, status_code):

    response = await ac.get(f"/hotels/{location}", params={"date_from": date_from, "date_to": date_to})

    assert response.status_code == status_code