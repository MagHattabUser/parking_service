from typing import List
import logging
import asyncio
from web.schemas import CameraParkingPlaceCreate, CameraParkingPlaceResponse
from application.services.interfaces.i_camera_parking_place_service import ICameraParkingPlaceService
from infrastructure.repositories.camera_parking_place import CameraParkingPlaceRepository
from fastapi import HTTPException
from web.mapper import CameraParkingPlaceMapper
from domain.models import CameraParkingPlace
import base64
import requests
from infrastructure.utils.s3_utils import get_image_from_minio
from infrastructure.utils.rabbitmq_utils import rabbitmq_client
from web.config import Configs

config = Configs()
logger = logging.getLogger(__name__)

class CameraParkingPlaceService(ICameraParkingPlaceService):
    async def create_link(self, data: CameraParkingPlaceCreate) -> CameraParkingPlaceResponse:
        self._validate_polygon(data.location)
        camera_parking_place = self.mapper.to_entity(data)
        created_link = await self.camera_parking_place_repo.save(camera_parking_place)
        return self.mapper.to_response(created_link)

    async def list_places_for_camera(self, camera_id: int) -> List[CameraParkingPlaceResponse]:
        links = await self.camera_parking_place_repo.list_places_by_camera(camera_id)
        return [self.mapper.to_response(link) for link in links]

    async def list_cameras_for_place(self, place_id: int) -> List[CameraParkingPlaceResponse]:
        links = await self.camera_parking_place_repo.list_cameras_by_place(place_id)
        return [self.mapper.to_response(link) for link in links]

    def __init__(self, camera_parking_place_repo: CameraParkingPlaceRepository):
        self.camera_parking_place_repo = camera_parking_place_repo
        self.mapper = CameraParkingPlaceMapper()

    def _validate_polygon(self, coordinates: List[List[float]]) -> None:
        if not coordinates or len(coordinates) < 3:
            raise HTTPException(status_code=400, detail="Polygon must have at least 3 points")
        if coordinates[0] != coordinates[-1]:
            raise HTTPException(status_code=400, detail="Polygon is not closed (first and last points must be the same)")

    async def create_camera_parking_place(self, data: CameraParkingPlaceCreate) -> CameraParkingPlaceResponse:
        self._validate_polygon(data.location)
        camera_parking_place = self.mapper.to_entity(data)
        created_camera_parking_place = await self.camera_parking_place_repo.save(camera_parking_place)
        return self.mapper.to_response(created_camera_parking_place)

    async def get_camera_parking_place(self, camera_parking_place_id: int) -> CameraParkingPlaceResponse:
        camera_parking_place = await self.camera_parking_place_repo.get_by_id(CameraParkingPlace, camera_parking_place_id)
        if not camera_parking_place:
            raise ValueError(f"CameraParkingPlace with id {camera_parking_place_id} not found")
        return self.mapper.to_response(camera_parking_place)

    async def get_all_camera_parking_places(self) -> List[CameraParkingPlaceResponse]:
        camera_parking_places = await self.camera_parking_place_repo.get_by_all(CameraParkingPlace)
        return [self.mapper.to_response(camera_parking_place) for camera_parking_place in camera_parking_places]

    async def update_camera_parking_place(self, camera_parking_place_id: int, data: CameraParkingPlaceCreate) -> CameraParkingPlaceResponse:
        self._validate_polygon(data.location)
        camera_parking_place = await self.camera_parking_place_repo.get_by_id(CameraParkingPlace, camera_parking_place_id)
        if not camera_parking_place:
            raise ValueError(f"CameraParkingPlace with id {camera_parking_place_id} not found")
        
        updated_camera_parking_place = self.mapper.to_entity(data)
        updated_camera_parking_place.id = camera_parking_place_id
        
        updated_camera_parking_place = await self.camera_parking_place_repo.update(updated_camera_parking_place)
        return self.mapper.to_response(updated_camera_parking_place)

    async def delete_camera_parking_place(self, camera_parking_place_id: int) -> None:
        camera_parking_place = await self.camera_parking_place_repo.get_by_id(CameraParkingPlace, camera_parking_place_id)
        if not camera_parking_place:
            raise ValueError(f"CameraParkingPlace with id {camera_parking_place_id} not found")
        await self.camera_parking_place_repo.delete(camera_parking_place)

    async def get_marked_zone_image(self, zone_id: int) -> dict:
        try:
            logger.info(f"Getting marked zone image for zone_id: {zone_id}")
            image_url = f"images/test_{zone_id}.jpg"  # Заглушка
            
            logger.info("Fetching parking places from database")
            places = await self.camera_parking_place_repo.list_places_by_zone(zone_id)
            logger.info(f"Found {len(places)} places for zone_id {zone_id}")
            
            draw_places = []
            for place in places:
                try:
                    if place.parking_place is None:
                        logger.error(f"Parking place is None for camera_parking_place id={place.id}")
                        continue
                    
                    draw_places.append({
                        "place_id": place.parking_place.place_number,  # Используем номер места вместо id
                        "location": place.location,
                        "status": place.parking_place.place_status_id == 2  # 1 - свободно (True), 2 - занято (False)
                    })
                except Exception as place_error:
                    logger.exception(f"Error processing place {place.id}: {place_error}")
            
            logger.info(f"Created {len(draw_places)} draw places")
            
            draw_request = {
                "image_url": image_url,
                "places": draw_places
            }
            
            logger.info(f"Sending request to cutter service via RabbitMQ queue: {config.DRAW_QUEUE}")
            try:
                # Создаем временную очередь для ответа
                response_queue, future = await rabbitmq_client.create_response_queue()
                
                # Отправляем запрос в очередь обработки изображений
                await rabbitmq_client.publish_message(
                    queue_name=config.DRAW_QUEUE,
                    message=draw_request,
                    reply_to=response_queue
                )
                
                # Ждем ответа
                try:
                    # Ожидаем ответа с таймаутом в 30 секунд
                    response_data = await asyncio.wait_for(future, timeout=30.0)
                    
                    if "error" in response_data:
                        logger.error(f"Error from cutter service: {response_data['error']}")
                        raise HTTPException(status_code=500, detail=f"Ошибка от сервиса обработки: {response_data['error']}")
                    
                    marked_image_url = response_data.get("marked_image_url")
                    if not marked_image_url:
                        logger.error("Missing marked_image_url in response")
                        raise HTTPException(status_code=500, detail="Отсутствует URL размеченного изображения в ответе")
                    
                    logger.info(f"Successfully got marked image URL: {marked_image_url}")
                    
                    logger.info("Getting image from MinIO")
                    image_data = get_image_from_minio(marked_image_url)
                    
                    base64_image = base64.b64encode(image_data).decode('utf-8')
                    logger.info("Successfully encoded image to base64")
                    
                    return {
                        "image": base64_image,
                        "format": "base64"
                    }
                except asyncio.TimeoutError:
                    logger.error("Timeout waiting for response from cutter service")
                    raise HTTPException(status_code=504, detail="Таймаут ожидания ответа от сервиса обработки")
                finally:
                    # Всегда очищаем временную очередь
                    await rabbitmq_client.cleanup_response_queue(response_queue)
            except Exception as e:
                logger.exception(f"Error communicating with RabbitMQ: {e}")
                raise HTTPException(status_code=500, detail=f"Ошибка при работе с RabbitMQ: {str(e)}")
                
        except HTTPException as http_exc:
            # Re-raise HTTP exceptions as-is
            raise http_exc
        except Exception as e:
            logger.exception(f"Unexpected error in get_marked_zone_image: {e}")
            raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}") 