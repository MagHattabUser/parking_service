import aio_pika
import json
import uuid
import asyncio
from typing import Any, Dict, Callable, Awaitable
from web.config import Configs

config = Configs()

class RabbitMQClient:
    def __init__(self):
        self.connection = None
        self.channel = None
        self._response_queues = {}

    async def connect(self):
        if not self.connection:
            self.connection = await aio_pika.connect_robust(
                host=config.RABBITMQ_HOST,
                port=config.RABBITMQ_PORT,
                login=config.RABBITMQ_USER,
                password=config.RABBITMQ_PASSWORD,
                virtualhost=config.RABBITMQ_VHOST
            )
            self.channel = await self.connection.channel()

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def publish_message(self, queue_name: str, message: Dict[str, Any], reply_to: str = None):
        await self.connect()
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                reply_to=reply_to
            ),
            routing_key=queue_name
        )

    async def consume_messages(self, queue_name: str, callback: Callable[[Dict[str, Any]], Awaitable[None]], durable: bool = True, auto_delete: bool = False):
        await self.connect()
        queue = await self.channel.declare_queue(queue_name, durable=durable, auto_delete=auto_delete)
        
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        data = json.loads(message.body.decode())
                        await callback(data)
                    except Exception as e:
                        print(f"Error processing message: {e}")

    async def create_response_queue(self) -> tuple[str, asyncio.Future]:
        """Создает временную очередь для получения ответа и возвращает её имя и future для получения результата"""
        await self.connect()
        queue_name = f"response_queue_{uuid.uuid4()}"
        queue = await self.channel.declare_queue(queue_name, durable=False, auto_delete=True)
        
        future = asyncio.Future()
        
        async def callback(data):
            if not future.done():
                future.set_result(data)
        
        consume_task = asyncio.create_task(self.consume_messages(queue_name, callback, durable=False, auto_delete=True))
        self._response_queues[queue_name] = consume_task
        
        return queue_name, future

    async def cleanup_response_queue(self, queue_name: str):
        """Очищает временную очередь и отменяет её обработку"""
        if queue_name in self._response_queues:
            task = self._response_queues.pop(queue_name)
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

rabbitmq_client = RabbitMQClient() 