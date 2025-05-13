from abc import ABC, abstractmethod


class IBase(ABC):
    @abstractmethod
    async def get_by_id(self, model, model_id: int):
        pass

    @abstractmethod
    async def get_by_all(self, model):
        pass

    @abstractmethod
    async def save(self, instance):
        pass

    @abstractmethod
    async def delete(self, instance):
        pass

    @abstractmethod
    async def update(self, instance):
        pass