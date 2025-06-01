from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

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
from infrastructure.utils.rabbitmq_utils import rabbitmq_client
from application.background.violation_detection_service import ViolationDetectionService

logger = logging.getLogger(__name__)

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

@app.on_event("startup")
async def startup_event():
    # Глобальная переменная для доступа к сервису из shutdown_event
    global violation_detection_service
    
    try:
        logger.info("Connecting to RabbitMQ...")
        await rabbitmq_client.connect()
        logger.info("Successfully connected to RabbitMQ")
        
        # Инициализация фонового сервиса проверки нарушений
        logger.info("Initializing violation detection service...")
        # Получаем сервисы из контейнера через resolve()
        from application.services.interfaces.i_parking_zone_service import IParkingZoneService
        from application.services.interfaces.i_violation_service import IViolationService
        from application.services.interfaces.i_unified_auth_service import IUnifiedAuthService
        from application.services.interfaces.i_booking_service import IBookingService
        from application.services.interfaces.i_camera_service import ICameraService
        
        parking_zone_service = container.resolve(IParkingZoneService)
        violation_service = container.resolve(IViolationService)
        booking_service = container.resolve(IBookingService)
        
        # Создаем объект настроек
        from web.config import Configs
        settings = Configs()
        
        # Получаем сервис камер
        camera_service = container.resolve(ICameraService)

        # Создаем сервис с интервалом проверки 15 минут
        violation_detection_service = ViolationDetectionService(
            parking_zone_service=parking_zone_service,
            violation_service=violation_service,
            booking_service=booking_service,
            camera_service=camera_service,
            settings=settings,
            check_interval_minutes=15
        )
        
        # Запускаем фоновый сервис
        await violation_detection_service.start()
        logger.info("Violation detection service started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    try:
        # Останавливаем фоновый сервис проверки нарушений
        if 'violation_detection_service' in globals():
            logger.info("Stopping violation detection service...")
            await violation_detection_service.stop()
            logger.info("Violation detection service stopped")
            
        # Закрываем соединение с RabbitMQ
        logger.info("Closing RabbitMQ connection...")
        await rabbitmq_client.close()
        logger.info("RabbitMQ connection closed")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")