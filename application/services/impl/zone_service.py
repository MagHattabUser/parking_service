import os
import json
import base64
import uuid
import asyncio
import aiohttp
from typing import List, Union, Dict
from web.schemas import (
    ParkingZoneCreate, 
    ParkingZoneResponse, 
    ParkingZoneDetailedResponse, 
    PlaceStatusUpdateResponse,
    CutRequest,
    PlaceCut,
    S3ObjectRequest,
    PlaceImage
)
from application.services.interfaces.i_parking_zone_service import IParkingZoneService
from infrastructure.repositories.parking_zone import ParkingZoneRepository
from fastapi import HTTPException
from web.mapper import ParkingZoneMapper
from domain.models import ParkingZone
from web.config import Configs
from loguru import logger
from infrastructure.utils.rabbitmq_utils import rabbitmq_client

class ParkingZoneService(IParkingZoneService):
    def __init__(self, parking_zone_repo: ParkingZoneRepository):
        self.parking_zone_repo = parking_zone_repo
        self.mapper = ParkingZoneMapper()

    def _validate_polygon(self, coordinates: List[List[float]]) -> None:
        if not coordinates or len(coordinates) < 3:
            raise HTTPException(status_code=400, detail="Polygon must have at least 3 points")
        if coordinates[0] != coordinates[-1]:
            raise HTTPException(status_code=400, detail="Polygon is not closed (first and last points must be the same)")

    async def create_zone(self, data: ParkingZoneCreate) -> ParkingZoneResponse:
        #self._validate_polygon(data.location)
        zone = self.mapper.to_entity(data)
        created_zone = await self.parking_zone_repo.save(zone)
        return self.mapper.to_response(created_zone)

    async def get_zone(self, zone_id: int) -> ParkingZoneResponse:
        zone = await self.parking_zone_repo.get_by_id(ParkingZone, zone_id)
        if not zone:
            raise ValueError(f"Parking zone with id {zone_id} not found")
        return self.mapper.to_response(zone)

    async def get_all_zones(self) -> List[ParkingZoneResponse]:
        zones = await self.parking_zone_repo.get_by_all(ParkingZone)
        return [self.mapper.to_response(zone) for zone in zones]

    async def update_zone(self, zone_id: int, data: ParkingZoneCreate) -> ParkingZoneResponse:
        #self._validate_polygon(data.location)
        zone = await self.parking_zone_repo.get_by_id(ParkingZone, zone_id)
        if not zone:
            raise ValueError(f"Parking zone with id {zone_id} not found")
        
        updated_zone = self.mapper.to_entity(data)
        updated_zone.id = zone_id
        
        updated_zone = await self.parking_zone_repo.update(updated_zone)
        return self.mapper.to_response(updated_zone)

    async def delete_zone(self, zone_id: Union[int, str]) -> None:
        zone = await self.parking_zone_repo.get_by_id(ParkingZone, zone_id)
        if not zone:
            raise ValueError(f"Parking zone with id {zone_id} not found")
        await self.parking_zone_repo.delete(zone)

    async def get_zones_by_admin(self, admin_id: int) -> List[ParkingZoneResponse]:
        zones = await self.parking_zone_repo.list_by_admin(admin_id)
        return [self.mapper.to_response(zone) for zone in zones]

    async def get_detailed_info(self, zone_id: int) -> ParkingZoneDetailedResponse:
        result = await self.parking_zone_repo.get_zone_detailed(zone_id)
        if not result:
            raise ValueError(f"Parking zone with id {zone_id} not found")
            
        zone, zone_type, total_places, free_places, occupied_places, total_cameras = result
        
        return ParkingZoneDetailedResponse(
            id=zone.id,
            zone_name=zone.zone_name,
            type_name=zone_type.type_name,
            address=zone.address,
            start_time=zone.start_time,
            end_time=zone.end_time,
            price_per_minute=zone.price_per_minute,
            location=zone.location,
            total_places=total_places,
            free_places=free_places,
            occupied_places=occupied_places,
            total_cameras=total_cameras,
            update_time=zone.update_time
        )
        
    async def update_place_status(self, place_id: int, status_id: int) -> PlaceStatusUpdateResponse:
        """
        Обновить статус одного парковочного места
        
        Args:
            place_id: ID парковочного места
            status_id: ID статуса (1 - Свободно, 2 - Занято)
        """
        try:
            logger.info(f"Updating status for place {place_id} to status_id={status_id}")
            # Создаем словарь с одним местом для обновления
            place_status_updates = {place_id: status_id}
            updated = await self.parking_zone_repo.update_places_status(place_status_updates)
            if updated:
                logger.info(f"Successfully updated status for place {place_id} to {status_id}")
                return PlaceStatusUpdateResponse(
                    updated_places=1,
                    message=f"Successfully updated place {place_id} status"
                )
            else:
                logger.warning(f"Failed to update status for place {place_id}")
                return PlaceStatusUpdateResponse(
                    updated_places=0,
                    message=f"Failed to update place {place_id} status"
                )
        except Exception as e:
            logger.error(f"Error updating place status: {e}")
            return PlaceStatusUpdateResponse(
                updated_places=0,
                message=f"Error: {str(e)}"
            )
            
    async def update_zone_check_time(self, zone_id: int) -> bool:
        """
        Обновляет время последней проверки зоны
        
        Args:
            zone_id: ID зоны парковки
            
        Returns:
            bool: True если обновление прошло успешно, иначе False
        """
        try:
            logger.info(f"Updating last check time for zone {zone_id}")
            # Получаем зону
            zone = await self.parking_zone_repo.get_by_id(ParkingZone, zone_id)
            if not zone:
                logger.error(f"Zone {zone_id} not found")
                return False
                
            # Обновляем время последней проверки
            from datetime import datetime
            zone.update_time = datetime.now()
            
            # Сохраняем изменения
            await self.parking_zone_repo.update(zone)
            logger.info(f"Successfully updated check time for zone {zone_id} to {zone.update_time}")
            return True
        except Exception as e:
            logger.error(f"Error updating zone check time: {e}")
            return False

    async def get_places_by_zone(self, zone_id: int) -> List:
        """
        Получить список парковочных мест в зоне с их координатами
        
        Args:
            zone_id: ID зоны парковки
            
        Returns:
            Список кортежей (место, {"location": координаты})
        """
        logger.info(f"Getting places for zone {zone_id}")
        
        # Получаем места в зоне из репозитория
        place_tuples = await self.parking_zone_repo.get_places_by_zone(zone_id)
        
        if not place_tuples:
            logger.warning(f"No places found for zone {zone_id}")
            return []
            
        logger.info(f"Found {len(place_tuples)} places for zone {zone_id}")
        return place_tuples
        
    async def process_zone_image(self, zone_id: int) -> PlaceStatusUpdateResponse:
        """Обработать изображение зоны и обновить статусы парковочных мест.
        
        Этот метод выполняет следующие шаги:
        1. Получает заглушечное изображение зоны (в будущем будет получать с камеры)
        2. Получает все места в зоне с их координатами
        3. Отправляет REST запрос в сервис нарезки для получения изображений отдельных мест
        4. Для каждого полученного изображения места отправляет REST запрос в сервис классификации
        5. Обновляет статусы мест в базе данных на основе результатов классификации
        """
        settings = Configs()
        logger.info(f"Processing zone image for zone_id={zone_id}")
        
        # 1. Получаем заглушечное изображение зоны (в будущем будет реальное)
        # Предполагаем, что изображение хранится в MinIO или другом хранилище
        # Для заглушки используем фиксированный URL к тестовому изображению
        placeholder_image_url = "images/test.jpg"
        logger.debug(f"Using placeholder image: {placeholder_image_url}")
        
        # 2. Получаем все места в зоне с их координатами
        places_with_locations = await self.parking_zone_repo.get_places_by_zone(zone_id)
        
        if not places_with_locations:
            logger.warning(f"No parking places found for zone_id={zone_id}")
            return PlaceStatusUpdateResponse(updated_places=0, message="No parking places found in this zone")
        
        # Подготавливаем данные для запроса на нарезку
        cut_places = []
        for place, place_data in places_with_locations:
            # Если у места нет координат, пропускаем его
            if not place_data["location"]:
                logger.warning(f"Place id={place.id} has no location data")
                continue
                
            cut_places.append(PlaceCut(
                place_id=place.id,
                location=place_data["location"]
            ))
        
        if not cut_places:
            logger.warning("No places with valid location data found")
            return PlaceStatusUpdateResponse(updated_places=0, message="No places with valid location data")
        
        # 3. Отправляем запрос на нарезку изображений
        cut_request = CutRequest(
            image_url=placeholder_image_url,
            places=cut_places
        )
        
        try:
            # Используем RabbitMQ для взаимодействия с сервисом нарезки
            # Создаем уникальный идентификатор запроса, чтобы запросы разных пользователей не перемешались
            request_id = str(uuid.uuid4())
            logger.debug(f"Creating RabbitMQ response queue for request_id={request_id}")
            
            # Создаем временную очередь для получения ответа
            response_queue, future = await rabbitmq_client.create_response_queue()
            
            try:
                logger.debug(f"Sending cut request via RabbitMQ")
                # Добавляем request_id в запрос
                message = {
                    "request_id": request_id,
                    "data": cut_request.dict()
                }
                
                # Отправляем сообщение в очередь для сервиса нарезки с указанием очереди для ответа
                await rabbitmq_client.publish_message("cut_queue", message, reply_to=response_queue)
                
                # Ожидаем ответ с таймаутом 30 секунд
                try:
                    cut_response = await asyncio.wait_for(future, timeout=30.0)
                    place_images = cut_response.get("place_images", [])
                    logger.debug(f"Received cut response with {len(place_images)} place images")
                except asyncio.TimeoutError:
                    logger.error("Timeout waiting for cutter service response")
                    return PlaceStatusUpdateResponse(
                        updated_places=0, 
                        message="Cutter service timeout"
                    )
            finally:
                # Очищаем временную очередь
                await rabbitmq_client.cleanup_response_queue(response_queue)
                    
            if not place_images:
                logger.warning("No place images returned from cutter service")
                return PlaceStatusUpdateResponse(updated_places=0, message="No place images received")
                
            # 4. Для каждого изображения места отправляем запрос на классификацию через RabbitMQ
            place_status_updates = {}  # Словарь {place_id: status_id}
            
            for place_image in place_images:
                # Получаем имя файла из URL изображения
                filename = os.path.basename(place_image.get("image_url", ""))
                place_id = place_image.get("place_id")
                
                if not filename or not place_id:
                    logger.warning(f"Invalid place image data: {place_image}")
                    continue
                
                # Добавляем префикс к имени файла (как указал пользователь)
                filename = "cut_images/" + filename
                class_request = S3ObjectRequest(filename=filename)
                
                # Создаем уникальный идентификатор для этого запроса
                class_request_id = str(uuid.uuid4())
                logger.debug(f"Creating RabbitMQ response queue for classification request_id={class_request_id}, place_id={place_id}")
                
                # Создаем временную очередь для получения ответа
                class_response_queue, class_future = await rabbitmq_client.create_response_queue()
                
                try:
                    # Отправляем запрос на классификацию через RabbitMQ
                    logger.debug(f"Sending classification request for place_id={place_id}, filename={filename}")
                    
                    # Формируем сообщение в формате, который ожидает Director
                    # Важно: reply_to должен быть в самом сообщении, а не только в метаданных
                    class_message = {
                        "request_id": class_request_id,
                        "data": class_request.dict(),
                        "reply_to": class_response_queue  # Добавляем очередь ответа в само сообщение
                    }
                    
                    # Отправляем сообщение в очередь для сервиса классификации
                    # Также передаем reply_to и в метаданных для надежности
                    await rabbitmq_client.publish_message("classify_queue", class_message, reply_to=class_response_queue)
                    
                    # Ожидаем ответ с таймаутом 15 секунд
                    try:
                        classification = await asyncio.wait_for(class_future, timeout=15.0)
                        class_id = classification.get("class_id")
                        class_name = classification.get("class_name")
                        
                        logger.info(f"Place id={place_id} classified as {class_name} (id={class_id})")
                        
                        # Преобразуем class_id в status_id для нашей базы данных
                        # Предполагаем, что class_id=0 означает "свободно" (status_id=1),
                        # class_id=1 означает "занято" (status_id=2)
                        status_id = class_id + 1  # Простое отображение для примера
                        
                        # Добавляем в список обновлений
                        place_status_updates[place_id] = status_id
                    except asyncio.TimeoutError:
                        logger.error(f"Timeout waiting for classification response for place_id={place_id}")
                finally:
                    # Очищаем временную очередь
                    await rabbitmq_client.cleanup_response_queue(class_response_queue)
            
            # 5. Обновляем статусы мест в базе данных
            if not place_status_updates:
                logger.warning("No valid classifications received")
                return PlaceStatusUpdateResponse(updated_places=0, message="No valid classifications")
                
            updated_count = await self.parking_zone_repo.update_places_status(place_status_updates)
            logger.info(f"Updated {updated_count} parking places in zone_id={zone_id}")
            
            return PlaceStatusUpdateResponse(
                updated_places=updated_count,
                message=f"Successfully updated {updated_count} parking places"
            )
            
        except Exception as e:
            logger.exception(f"Error processing zone image: {str(e)}")
            return PlaceStatusUpdateResponse(
                updated_places=0,
                message=f"Error processing zone image: {str(e)}"
            )