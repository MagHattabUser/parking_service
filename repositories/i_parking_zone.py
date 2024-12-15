from abc import ABC, abstractmethod


class IParkingZone(ABC):
    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def delete_by_id_or_name(self, identifier: str | int):
        pass