from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from web.container import get_container
from web.handlers.admin import router as admin_router
from web.handlers.booking import router as booking_router
from web.handlers.booking_status import router as booking_status_router
from web.handlers.car import router as car_router
from web.handlers.car_user import router as car_user_router
from web.handlers.camera import router as camera_router
from web.handlers.camera_parking_place import router as camera_parking_place_router
from web.handlers.place_status import router as place_status_router
from web.handlers.user import router as user_router
from web.handlers.violation import router as violation_router
from web.handlers.zone_type import router as zone_type_router
from web.handlers.places import router as places_router
from web.handlers.zones import router as zones_router
from web.handlers.unified_auth import router as unified_auth_router

app = FastAPI(title="Parking Service API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

container = get_container()
app.include_router(unified_auth_router)
app.include_router(admin_router)
app.include_router(booking_router)
app.include_router(booking_status_router)
app.include_router(car_router)
app.include_router(car_user_router)
app.include_router(camera_router)
app.include_router(camera_parking_place_router)
app.include_router(place_status_router)
app.include_router(user_router)
app.include_router(violation_router)
app.include_router(zone_type_router)
app.include_router(places_router)
app.include_router(zones_router)