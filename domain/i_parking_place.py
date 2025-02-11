from abc import ABC, abstractmethod


class IParkingPlace(ABC):
    @abstractmethod
    async def get_by_zone(self, zone_identifier: str | int):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def delete_by_id(self, place_id: int):
        pass