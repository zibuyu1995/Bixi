import asyncio

import uvloop

from mode import Worker
from gravity.app import App


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()


app = App(node_id='test')


@app.timer(interval=1)
async def timer():
    print(1)


@app.timer(interval=2)
async def timer2():
    print(2)


if __name__ == '__main__':
    Worker(app, loglevel="info", loop=loop).execute_from_commandline()

