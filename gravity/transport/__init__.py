import asyncio
from weakref import WeakSet

from mode.utils.queues import FlowControlEvent, ThrowableQueue


class Channel:
    def __init__(self, loop):
        self.loop = loop
        self._queue = None

    @property
    def queue(self):
        maxsize = 1024
        if self._queue is None:
            self._queue = self.FlowControlQueue(
                maxsize=maxsize,
                loop=self.loop,
                clear_on_resume=False
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
            flow_control=FlowControlEvent(initially_suspended=False, loop=self.loop),
            clear_on_resume=clear_on_resume,
            loop=loop or self.loop,
        )

    async def put(self, value) -> None:
        await self.queue.put(value)

    async def get(self):
        return await self.queue.get()

    @property
    def size(self) -> int:
        return self.queue.qsize()

