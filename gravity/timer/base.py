# coding: utf-8

import time
import asyncio


loop = asyncio.get_event_loop()

_futures = set()


async def timers():
    while True:
        print(1)
        await asyncio.sleep(1)


async def _execute_task(task) -> None:
    try:
        await task
    except asyncio.CancelledError:
        ...
    except RuntimeError as exc:
        ...
    except BaseException as exc:
        ...


def on_future_done(fut):
    _futures.discard(fut)


async def add_future():
    fut = await asyncio.ensure_future(_execute_task(timers()), loop=loop)
    fut.__wrapped__ = timers()
    fut.add_done_callback(on_future_done)
    _futures.add(fut)
    return fut


if __name__ == '__main__':
    loop.run_until_complete(add_future())


