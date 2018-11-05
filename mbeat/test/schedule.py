#!/usr/bin/env python
# coding: utf-8

"""
redis 定时任务
"""

import time
import asyncio
from concurrent.futures import ProcessPoolExecutor
import logging
import sys

from aioredis import create_redis
from datetime import datetime
from utils.send_task import test_task


async def connect_redis(loop):
    redis_store = await create_redis('redis://:public@localhost:6379/10')
    return redis_store


async def poll_schedule_tasks(loop, period, executor):
    """
    定期轮询
    """
    log = logging.getLogger('run_blocking_tasks')
    # redis_store = await connect_redis(loop)
    while True:
        now = datetime.now()
        print(now)
        score = int(time.time())
        # await redis_store.zadd('schedule_task', score, str(now))
        # await asyncio.sleep(period)
        # a = await redis_store.zrangebyscore('schedule_task')
        process_loop = asyncio.get_event_loop()
        blocking_tasks = [
            process_loop.run_in_executor(executor, test_task, i)
            for i in range(4)
        ]
        completed, pending = await asyncio.wait(blocking_tasks)
        results = [t.result() for t in completed]
        print(results)
        await asyncio.sleep(period)


async def main(loop, period, executor):
    await poll_schedule_tasks(loop, period, executor)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='PID %(process)5s %(name)18s: %(message)s',
        stream=sys.stderr,
    )
    period = 1
    executor = ProcessPoolExecutor(
        max_workers=4,
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        main(loop, 1, executor)
    )
    loop.close()
