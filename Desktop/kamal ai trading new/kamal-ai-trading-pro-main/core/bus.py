from __future__ import annotations
import asyncio
from collections import defaultdict
from typing import Any, DefaultDict

class EventBus:
    def __init__(self):
        self._queues: DefaultDict[str, asyncio.Queue] = defaultdict(lambda: asyncio.Queue())

    def topic(self, name: str) -> asyncio.Queue:
        return self._queues[name]

    async def publish(self, topic: str, item: Any) -> None:
        await self.topic(topic).put(item)

    def publish_nowait(self, topic: str, item: Any) -> None:
        self.topic(topic).put_nowait(item)

    async def listen(self, topic: str, handler):
        q = self.topic(topic)
        while True:
            item = await q.get()
            try:
                res = handler(item)
                if asyncio.iscoroutine(res):
                    await res
            finally:
                q.task_done()

global_bus = EventBus()
