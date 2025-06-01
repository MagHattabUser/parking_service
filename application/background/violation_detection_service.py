import asyncio
import uuid
from datetime import datetime, timedelta
import os
from typing import List, Dict, Optional, Set

import aiohttp
from loguru import logger

from web.config import Configs
from web.schemas import (
    CutRequest, 
    PlaceCut, 
    S3ObjectRequest, 
    DetectionResponse,
    ViolationCreate
)
from application.services.interfaces.i_parking_zone_service import IParkingZoneService
from application.services.interfaces.i_violation_service import IViolationService
from application.services.interfaces.i_booking_service import IBookingService
from application.services.interfaces.i_camera_service import ICameraService
from infrastructure.utils.rabbitmq_utils import rabbitmq_client

class ViolationDetectionService:
    def __init__(self, 
                 parking_zone_service: IParkingZoneService,
                 violation_service: IViolationService,
                 booking_service: IBookingService,
                 camera_service: ICameraService,
                 settings: Configs,
                 check_interval_minutes: int = 15):
        self.parking_zone_service = parking_zone_service
        self.violation_service = violation_service
        self.booking_service = booking_service
        self.camera_service = camera_service
        self.settings = settings
        self.check_interval_minutes = check_interval_minutes
        self.is_running = False
        self.task = None

    async def start(self):
        """Запуск фонового сервиса"""
        if self.is_running:
            logger.warning("Violation detection service is already running")
            return
        
        self.is_running = True
        self.task = asyncio.create_task(self._run_periodic_check())
        logger.info(f"Violation detection service started with interval {self.check_interval_minutes} minutes")

    async def stop(self):
        """Остановка фонового сервиса"""
        if not self.is_running:
            logger.warning("Violation detection service is not running")
            return
        
        self.is_running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        logger.info("Violation detection service stopped")

    async def _run_periodic_check(self):
        """Периодическая проверка нарушений"""
        while self.is_running:
            try:
                logger.info("Starting violation detection check...")
                await self._check_all_zones()
                logger.info("Violation detection check completed")
            except Exception as e:
                logger.error(f"Error in violation detection service: {e}")
            
            # Ждем указанный интервал времени перед следующей проверкой
            await asyncio.sleep(self.check_interval_minutes * 60)
    
    async def _check_all_zones(self):
        """Проверка всех парковочных зон на наличие нарушений"""
        # Получаем все парковочные зоны
        zones = await self.parking_zone_service.get_all_zones()
        logger.info(f"Found {len(zones)} parking zones to check")
        
        # Получаем текущее время для фильтрации активных бронирований
        current_time = datetime.now()
        
        # Получаем все активные бронирования на текущий момент
        active_bookings = await self.booking_service.get_active_bookings(current_time)
        
        # Создаем сет забронированных мест для быстрой проверки
        booked_place_ids = {booking.parking_place_id for booking in active_bookings}
        logger.info(f"Found {len(booked_place_ids)} currently booked places")
        
        for zone in zones:
            logger.info(f"Checking zone {zone.zone_name} (ID: {zone.id})")
            await self._check_zone(zone.id, booked_place_ids)

    async def _check_zone(self, zone_id: int, booked_place_ids: set):
        """Проверка одной зоны на нарушения"""
        try:
            # Получаем информацию о зоне
            zone = await self.parking_zone_service.get_zone(zone_id)
            if not zone:
                logger.error(f"Zone with ID {zone_id} not found")
                return
            
            # Получаем все места в зоне с их координатами
            place_tuples = await self.parking_zone_service.get_places_by_zone(zone_id)
            if not place_tuples:
                logger.info(f"No places found in zone {zone.zone_name} (ID: {zone_id})")
                return
            
            logger.info(f"Found {len(place_tuples)} places in zone {zone.zone_name}")
            
            # Фильтруем только незабронированные места
            # Здесь мы извлекаем объект места из кортежа для проверки ID
            places_to_check = [place_tuple for place_tuple in place_tuples 
                              if place_tuple[0].id not in booked_place_ids]
            logger.info(f"Checking {len(places_to_check)} non-booked places in zone {zone.zone_name}")
            
            # Получаем изображения с камер зоны для анализа
            try:
                # Получаем снимки с всех камер зоны
                snapshots = await self.camera_service.get_zone_snapshots(zone_id)
                if not snapshots:
                    logger.warning(f"No camera snapshots available for zone {zone_id}, skipping")
                    return
                    
                # Для простоты используем первый снимок с первой камеры
                # В реальном приложении можно будет обрабатывать все снимки
                # или выбирать снимок с конкретной камеры для каждого места
                first_camera_id = next(iter(snapshots.keys()))
                image_data = snapshots[first_camera_id]
                
                # Сохраняем изображение в MinIO и получаем URL
                # Для простоты используем фиксированный URL
                # В реальном приложении здесь будет загрузка изображения в S3/MinIO
                image_url = "images/test.jpg"
                logger.info(f"Got camera snapshot for zone {zone_id}, camera {first_camera_id}")
            except Exception as e:
                logger.error(f"Error getting camera snapshots for zone {zone_id}: {e}")
                # Используем запасной вариант с тестовым изображением
                image_url = "images/test.jpg"

            # Проверяем каждое незабронированное место
            for place_tuple in places_to_check:
                # Отправляем запрос на вырезание изображения места в Cutter сервис
                await self._process_place(zone, place_tuple, image_url)
                
            # Обновляем время последней проверки зоны
            update_success = await self.parking_zone_service.update_zone_check_time(zone_id)
            if update_success:
                logger.info(f"Updated last check time for zone {zone_id}")
            else:
                logger.warning(f"Failed to update last check time for zone {zone_id}")
                
        except Exception as e:
            logger.error(f"Error checking zone {zone_id}: {e}")
    
    async def _process_place(self, zone, place_tuple, image_url: str):
        """Обработка одного парковочного места"""
        try:
            # Распаковываем кортеж (место, {"location": координаты})
            place, place_data = place_tuple
            location = place_data.get("location")
            
            logger.info(f"Processing place {place.id} in zone {zone.zone_name} (ID: {zone.id})")

            # Проверяем, есть ли координаты для места
            if not location:
                logger.error(f"Place {place.id} has no location coordinates, skipping")
                return
            
            # Формируем уникальный идентификатор запроса
            request_id = str(uuid.uuid4())
            
            # Создаем временную очередь для ответа (как в ZoneService.process_zone_image)
            response_queue, future = await rabbitmq_client.create_response_queue()
            
            # Формируем запрос на вырезание изображения в соответствии со схемой
            # Создаем данные запроса
            cut_data = {
                "image_url": image_url,
                "places": [
                    {
                        "place_id": place.id,
                        "location": location
                    }
                ]
            }
            
            # Оборачиваем в структуру с ключом "data", как ожидает Cutter сервис
            cut_request = {
                "request_id": request_id,
                "data": cut_data
            }
            
            # Отправляем запрос в Cutter сервис через RabbitMQ
            # Используем очередь "cut_queue" вместо DRAW_QUEUE и указываем reply_to
            await rabbitmq_client.publish_message(
                "cut_queue",
                cut_request,
                reply_to=response_queue
            )
            logger.info(f"Sent cut request for place {place.id} to Cutter service, request_id: {request_id}")
            
            try:
                # Ожидаем ответ с таймаутом
                result = await asyncio.wait_for(future, timeout=30)
                if not result:
                    logger.error(f"Empty response from Cutter service for place {place.id}")
                    return
            except asyncio.TimeoutError:
                logger.error(f"Timeout waiting for Cutter service response for place {place.id}")
                return
            finally:
                # Очищаем временную очередь
                try:
                    await rabbitmq_client.cleanup_response_queue(response_queue)
                except Exception as e:
                    logger.error(f"Failed to cleanup response queue: {e}")
            
            # Получаем информацию о вырезанном изображении
            # Обрабатываем ответ в зависимости от формата ответа
            image_url = None
            try:
                if isinstance(result, dict):
                    # Прямой ответ с URL изображения
                    if "place_images" in result:
                        # Формат ответа из process_zone_image
                        place_images = result.get("place_images", [])
                        logger.debug(f"Ответ от Cutter сервиса: {result}")
                        for img_data in place_images:
                            if img_data.get("place_id") == place.id:
                                image_url = img_data.get("image_url")
                                logger.info(f"Найден URL изображения для места {place.id}: {image_url}")
                                break
                    else:
                        # Прямой ответ с URL изображения
                        image_url = result.get("image_url")
                elif isinstance(result, list) and len(result) > 0:
                    # Список ответов, берем первый
                    item = result[0]
                    if isinstance(item, dict):
                        image_url = item.get("image_url")
            except Exception as e:
                logger.error(f"Error parsing Cutter service response for place {place.id}: {e}")
                return
                    
            if not image_url:
                logger.error(f"No image URL in Cutter service response for place {place.id}")
                return
                
            logger.info(f"Received cut result for place {place.id}, image_url: {image_url}")
            
            # Отправляем запрос в Director сервис через REST API
            detection_result = await self._detect_car(image_url)
            if not detection_result:
                logger.error(f"Failed to get detection result for place {place.id}")
                return
                
            # Обрабатываем результат распознавания
            await self._process_detection_result(place, detection_result)
        except Exception as e:
            logger.error(f"Error processing place {place.id}: {e}")
    
    async def _detect_car(self, object_name: str) -> DetectionResponse:
        """Отправляет запрос в Director сервис для распознавания автомобиля"""
        try:
            # Используем aiohttp для асинхронных HTTP запросов
            async with aiohttp.ClientSession() as session:
                url = f"{self.settings.DIRECTOR_SERVICE_URL}/detect"
                logger.info(f"Sending detection request to Director service: {url}")
                
                # Формируем JSON с именем объекта для распознавания
                # Используем 'filename' вместо 'file' согласно требованию API Director сервиса
                payload = {"filename": object_name}
                
                # Отправляем POST запрос
                async with session.post(url, json=payload) as response:
                    if response.status != 200:
                        logger.error(f"Director service returned error: {response.status} {await response.text()}")
                        return None
                    
                    # Парсим ответ в DetectionResponse
                    data = await response.json()
                    logger.info(f"Received detection response from Director service: {data}")
                    
                    try:
                        # Адаптируем формат ответа Director к нашей модели DetectionResponse
                        # Добавляем подробное логирование полей ответа
                        logger.info(f"Director response type: {type(data)}")
                        logger.info(f"Director response content: {data}")
                        logger.info(f"Director response fields - status: {data.get('status')}, parking_status: {data.get('parking_status')}")
                        
                        # Используем parking_status напрямую из ответа Director
                        parking_status = data.get("parking_status", "Неизвестно")
                        logger.info(f"Extracted parking_status value: {parking_status}")
                        
                        adapted_data = {
                            "status": data.get("status", "unknown"),
                            "parking_status": parking_status,
                            "plate_number": data.get("plate_number")
                        }
                        
                        detection_response = DetectionResponse(**adapted_data)
                        logger.info(f"Parsed detection response: status={detection_response.status}, "
                                   f"parking_status={detection_response.parking_status}, "
                                   f"plate_number={detection_response.plate_number if detection_response.plate_number else 'None'}")
                        return detection_response
                    except Exception as e:
                        logger.error(f"Failed to parse detection response: {e}, raw data: {data}")
                        return None
        except Exception as e:
            logger.error(f"Error during car detection: {e}")
            return None
    
    async def _process_detection_result(self, place, detection: DetectionResponse):
        """Обрабатывает результат распознавания и создает нарушение при необходимости"""
        try:
            # Проверяем статус места
            logger.info(f"Processing detection result for place {place.id}, status: {detection.parking_status}")
            logger.info(f"Checking if parking_status '{detection.parking_status}' equals 'Занято'")
            
            # Проверяем статус независимо от регистра и возможных пробелов
            if detection.parking_status and detection.parking_status.strip().lower() == "занято":
                # Место занято, но не забронировано - это нарушение
                logger.info(f"Detected violation at place {place.id}: car with number {detection.plate_number}")
                
                # Проверяем, есть ли уже нарушение для этого места и номера за последние 2 часа
                existing_violations = await self.violation_service.list_by_place(place.id)
                
                # Фильтруем по номеру и времени (не более 2 часов назад)
                current_time = datetime.now()
                two_hours_ago = current_time - timedelta(hours=2)
                
                recent_same_car_violation = False
                for violation in existing_violations:
                    if (violation.car_number == detection.plate_number and 
                        violation.timestamp >= two_hours_ago):
                        recent_same_car_violation = True
                        break
                
                # Если нет недавнего нарушения для этого же авто, создаем новое
                if not recent_same_car_violation:
                    # Добавляем текущее время в timestamp
                    violation_data = ViolationCreate(
                        parking_place_id=place.id,
                        car_number=detection.plate_number,
                        description=f"Незаконная парковка на месте {place.id}",
                        timestamp=datetime.now()
                    )
                    await self.violation_service.create_violation(violation_data)
                    logger.info(f"Created new violation record for place {place.id}, car number: {detection.plate_number}")
                else:
                    logger.info(f"Skipped duplicate violation for place {place.id}, car number: {detection.plate_number}")
                
                # Обновляем статус места на "Занято"
                await self.parking_zone_service.update_place_status(place.id, 2)  # Статус "Занято" имеет id = 2
            # Проверяем свободно ли место
            elif detection.parking_status and detection.parking_status.strip().lower() == "свободно":
                # Место свободно, обновляем статус
                logger.info(f"Place {place.id} is free")
                await self.parking_zone_service.update_place_status(place.id, 1)  # Статус "Свободно" имеет id = 1
        except Exception as e:
            logger.error(f"Error processing detection result for place {place.id}: {e}")