from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from redis import asyncio as aioredis

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms

from app.pages.router import router as pages_router
from app.images.router import router as image_router


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(pages_router)
app.include_router(image_router)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

@app.on_event("startup")
async def startup():
    redis = await aioredis.from_url("redis://localhost:6379", encoding="utf8")
    FastAPICache.init(RedisBackend(redis), prefix="cache")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
