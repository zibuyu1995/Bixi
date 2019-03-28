# coding: utf-8

import asyncio
from weakref import WeakSet

from mode.utils.queues import FlowControlEvent, ThrowableQueue


class Channel:
    def __init__(self, loop):
        self.loop = loop
        self._queue = None
        self._subscribers = WeakSet()
        ...

    @property
    def queue(self):
        maxsize = 1024
        self._queue = self.FlowControlQueue(
            maxsize=maxsize,
            loop=self.loop,
            clear_on_resume=True
        )
        return self._queue

    def FlowControlQueue(
            self,
            maxsize: int = None,
            *,
            clear_on_resume: bool = False,
            loop: asyncio.AbstractEventLoop = None) -> ThrowableQueue:
        """Like :class:`asyncio.Queue`, but can be suspended/resumed."""

        return ThrowableQueue(
            maxsize=maxsize,
            flow_control=FlowControlEvent(loop=self.loop),
            clear_on_resume=clear_on_resume,
            loop=loop or self.loop,
        )

    async def put(self, value) -> None:
        await self.queue.put(value)

    async def get(self):
        return await self.queue.get()

    @property
    def subscriber_count(self) -> int:
        return len(self._subscribers)


async def main(event_loop):
    chanel = Channel(event_loop)
    for i in range(10):
        await chanel.put(i)
    while True:
        await chanel.get()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
