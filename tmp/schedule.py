#!/usr/bin/env python
# coding: utf-8

"""
redis 定时任务
"""

import time
import asyncio

from aioredis import create_redis
from datetime import datetime


async def connect_redis(loop):
    redis_store = await create_redis('redis://:public@localhost:6379/10')
    return redis_store


async def poll_schedule_tasks(loop, period):
    """
    定期轮询
    """
    redis_store = await connect_redis(loop)
    while True:
        now = datetime.now()
        print(now)
        score = int(time.time())
        await redis_store.zadd('schedule_task', score, str(now))
        await asyncio.sleep(period)
        a = await redis_store.zrangebyscore('schedule_task')
        print(a)


async def main(loop, period):
    await poll_schedule_tasks(loop, period)


if __name__ == '__main__':
    period = 1
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop, period))
    loop.close()
