import asyncio
from functools import wraps, partial

from mode import Service
from gravity.transport import Channel

from gravity.utils.cron import secs_for_next


class Agent(Service):
    def __init__(self, channel, *, loop=None):
        self.channel = channel
        super().__init__(loop=loop)

    async def on_start(self):
        while True:
            print(await self.channel.get())

    async def on_stop(self):
        ...




