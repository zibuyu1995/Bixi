# coding: utf-8

from datetime import datetime
import asyncio
from typing import AnyStr, Any
from mode import Worker
from mode.threads import ServiceThread


class OneThread(ServiceThread):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    async def on_start(self) -> None:
        print('start one server')

    async def on_thread_stop(self) -> None:
        # on_stop() executes in parent thread, on_thread_stop in the thread.
        print('stop one server')


class TwoThread(ServiceThread):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    async def on_start(self) -> None:
        print('start two server')
        while True:
            await asyncio.sleep(1)
            print('two server')

    async def on_thread_stop(self) -> None:
        # on_stop() executes in parent thread, on_thread_stop in the thread.
        print('stop two server')


class ThreeThread(ServiceThread):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    async def on_start(self) -> None:
        print('start three server')
        while True:
            await asyncio.sleep(1)
            print('three server')

    async def on_thread_stop(self) -> None:
        # on_stop() executes in parent thread, on_thread_stop in the thread.
        print('stop three server')


if __name__ == '__main__':
    Worker(OneThread(), TwoThread(), ThreeThread(), loglevel="info").execute_from_commandline()
