import asyncio
from functools import wraps, partial

from mode import Service
from mode.timers import timer_intervals
from mode.utils.objects import qualname

from bixi.utils.cron import secs_for_next


class App(Service):
    channel = None
    _tasks = None

    def __init__(self, node_id, *, loop=None):
        self.node_id = node_id
        self._tasks = []
        super().__init__(loop=loop)

    def task(self, func):
        def _inner(func):
            return self._task(func)
        return _inner(func)

    def _task(self, func):
        @wraps(func)
        async def _wrapped():
            return await func()
        self._tasks.append(_wrapped)
        return _wrapped

    def timer(self, func=None, interval=60):
        if func is None:
            return partial(self.timer, interval=interval)
        timer_name = qualname(func)

        @wraps(func)
        async def _wrapped(*args, **kwargs):
            await self.sleep(interval)
            for sleep_time in timer_intervals(
                    interval, name=timer_name,
                    max_drift_correction=0.1):
                if self.should_stop:
                    break
                await func(*args, **kwargs)
                await self.sleep(sleep_time)
                if self.should_stop:
                    break
        self.task(_wrapped)
        return _wrapped

    def crontab(self, func=None, cron_format: str = None, **kwargs):
        if func is None:
            return partial(self.crontab, cron_format=cron_format, **kwargs)

        @wraps(func)
        async def _wrapped():
            while not self.should_stop:
                next_time = secs_for_next(cron_format)
                await asyncio.sleep(next_time)
                await func()
        self.task(_wrapped)
        return _wrapped

    async def send(self, send_value):
        ...

    def _channel(self):
        ...

    def _agent(self):
        ...

    def load_config(self):
        ...

    async def on_started(self):
        for task in self._tasks:
            self.add_future(task())

    async def on_stop(self):
        ...
