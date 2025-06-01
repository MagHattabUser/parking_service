from abc import ABC, abstractmethod
from typing import List, Union
from web.schemas import ParkingZoneCreate, ParkingZoneResponse, ParkingZoneDetailedResponse, PlaceStatusUpdateResponse

class IParkingZoneService(ABC):
    @abstractmethod
    async def create_zone(self, data: ParkingZoneCreate) -> ParkingZoneResponse:
        pass

    @abstractmethod
    async def get_zone(self, zone_id: int) -> ParkingZoneResponse:
        pass

    @abstractmethod
    async def get_all_zones(self) -> List[ParkingZoneResponse]:
        pass

    @abstractmethod
    async def update_zone(self, zone_id: int, data: ParkingZoneCreate) -> ParkingZoneResponse:
        pass

    @abstractmethod
    async def delete_zone(self, zone_id: Union[int, str]) -> None:
        pass

    @abstractmethod
    async def get_zones_by_admin(self, admin_id: int) -> List[ParkingZoneResponse]:
        pass

    @abstractmethod
    async def get_detailed_info(self, zone_id: int) -> ParkingZoneDetailedResponse:
        pass
        
    @abstractmethod
    async def process_zone_image(self, zone_id: int) -> PlaceStatusUpdateResponse:
        """Обработать изображение зоны и обновить статусы парковочных мест
        
        1. Получить изображение зоны (сейчас заглушка)
        2. Отправить запрос на нарезку изображений мест
        3. Получить результаты нарезки
        4. Для каждого изображения места отправить запрос на классификацию
        5. Получить результаты классификации
        6. Обновить статусы мест в базе данных
        
        Args:
            zone_id: ID зоны парковки
            
        Returns:
            Информация о количестве обновленных мест
        """
        pass
        
    @abstractmethod
    async def update_place_status(self, place_id: int, status_id: int) -> None:
        """Обновить статус парковочного места
        
        Args:
            place_id: ID парковочного места
            status_id: ID статуса (1 - Свободно, 2 - Занято)
            
        Returns:
            None
        """
        pass
        
    @abstractmethod
    async def get_places_by_zone(self, zone_id: int) -> List:
        """Получить список парковочных мест в зоне
        
        Args:
            zone_id: ID зоны парковки
            
        Returns:
            Список парковочных мест
        """
        pass