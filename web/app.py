import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from application.background.violation_detection_service import ViolationDetectionService
from application.services.interfaces.i_booking_service import IBookingService
from application.services.interfaces.i_camera_service import ICameraService
from application.services.interfaces.i_parking_place_service import IParkingPlaceService
from application.services.interfaces.i_parking_zone_service import IParkingZoneService
from application.services.interfaces.i_violation_service import IViolationService
from infrastructure.utils.rabbitmq_utils import rabbitmq_client
from web.config import Configs
from web.container import get_container
from web.handlers.admin import router as admin_router
from web.handlers.booking import router as booking_router
from web.handlers.booking_status import router as booking_status_router
from web.handlers.camera import router as camera_router
from web.handlers.camera_parking_place import router as camera_parking_place_router
from web.handlers.car import router as car_router
from web.handlers.car_user import router as car_user_router
from web.handlers.place_status import router as place_status_router
from web.handlers.places import router as places_router
from web.handlers.unified_auth import router as unified_auth_router
from web.handlers.user import router as user_router
from web.handlers.violation import router as violation_router
from web.handlers.zone_type import router as zone_type_router
from web.handlers.zones import router as zones_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting application...")
    container = get_container()
    app.state.container = container

    try:
        logger.info("Connecting to RabbitMQ...")
        await rabbitmq_client.connect()
        logger.info("Successfully connected to RabbitMQ")

        # Инициализация сервисов
        settings: Configs = container.resolve(Configs)
        parking_zone_service: IParkingZoneService = container.resolve(IParkingZoneService)
        violation_service: IViolationService = container.resolve(IViolationService)
        booking_service: IBookingService = container.resolve(IBookingService)
        camera_service: ICameraService = container.resolve(ICameraService)
        parking_place_service: IParkingPlaceService = container.resolve(IParkingPlaceService)

        # Настройка и запуск сервиса обнаружения нарушений
        violation_detection_service = ViolationDetectionService(
            parking_zone_service=parking_zone_service,
            violation_service=violation_service,
            booking_service=booking_service,
            camera_service=camera_service,
            settings=settings,
            check_interval_minutes=15
        )
        await violation_detection_service.start()
        app.state.violation_detection_service = violation_detection_service
        logger.info("Violation detection service started successfully")

        # Настройка и запуск планировщика для автоматизации статусов
        scheduler = AsyncIOScheduler()
        scheduler.add_job(
            parking_place_service.automate_place_statuses,
            'interval',
            minutes=1,
            id="automate_place_statuses_job"
        )
        scheduler.add_job(
            booking_service.complete_expired_bookings,
            'interval',
            minutes=1,
            id="complete_expired_bookings_job"
        )
        scheduler.start()
        app.state.scheduler = scheduler
        logger.info("APScheduler for status automation started")

    except Exception as e:
        logger.error(f"Failed to initialize services: {e}", exc_info=True)

    yield

    # Shutdown
    logger.info("Shutting down application...")
    if hasattr(app.state, 'scheduler') and app.state.scheduler.running:
        logger.info("Stopping APScheduler...")
        app.state.scheduler.shutdown()
        logger.info("APScheduler stopped")

    if hasattr(app.state, 'violation_detection_service'):
        logger.info("Stopping violation detection service...")
        await app.state.violation_detection_service.stop()
        logger.info("Violation detection service stopped")

    logger.info("Closing RabbitMQ connection...")
    await rabbitmq_client.close()
    logger.info("RabbitMQ connection closed")


app = FastAPI(title="Parking Service API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
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