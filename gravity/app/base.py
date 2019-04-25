import asyncio
from functools import wraps, partial

from mode import Service

from gravity.transport import Channel
from gravity.utils.cron import secs_for_next
from .agent import Agent


class App(Service):
    channel = None

    def __init__(self, node_id, *, loop=None):
        self.node_id = node_id
        super().__init__(loop=loop)

    def timer(self, func=None, interval=60):
        if func is None:
            return partial(self.timer, interval=interval)

        @wraps(func)
        async def decorated(*args, **kwargs):
            while True:
                await asyncio.sleep(interval)
                await func(*args, **kwargs)

        return self.add_future(decorated())

    def crontab(self, func=None, cron_format: str = None, timezone=None):
        if func is None:
            return partial(self.crontab, cron_format, timezone=timezone)

        @wraps(func)
        async def decorated(*args, **kwargs):
            while True:
                await asyncio.sleep(secs_for_next(cron_format, timezone))
                await func(*args, **kwargs)

        return self.add_future(decorated())

    async def send(self, send_value):
        await self.channel.put(send_value)

    def _channel(self):
        return Channel(loop=self.loop)

    def _agent(self):
        return Agent(self.channel)

    def on_init_dependencies(self):
        self.channel = self._channel()
        return [self._agent()]
