from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):

    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    can_delete = False
    column_details_exclude_list = [Users.hashed_password]
    column_list = [Users.id, Users.email, Users.booking]


class BookingsAdmin(ModelView, model=Bookings):

    name = "Бронь"
    name_plural = "Брони"
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user]
    icon = "fa-solid fa-book"


class RoomsAdmin(ModelView, model=Rooms):

    name = "Комната"
    name_plural = "Комнаты"
    can_delete = False
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.booking, Rooms.hotel]
    icon = "fa-solid fa-bed"


class HotelsAdmin(ModelView, model=Hotels):

    name = "Отель"
    name_plural = "Отели"
    can_delete = False
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.room]
    icon = "fa-solid fa-hotel"



