import asyncio

import uvloop
import datetime

from mode import Worker
from gravity.app import App
from gravity.app.agent import Agent


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()


app = App(node_id='test')


@app.timer(interval=1)
async def timer():
    await app.send(datetime.datetime.now())


if __name__ == '__main__':
    Worker(app, Agent(channel=channel), loglevel="info", loop=loop).execute_from_commandline()

