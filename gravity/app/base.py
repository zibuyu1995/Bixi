import asyncio
from functools import wraps, partial

from mode import Service

from gravity.utils.cron import secs_for_next


class App(Service):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(App, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

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
