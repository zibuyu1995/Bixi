import asyncio
from datetime import datetime

import uvloop

from gravity.app import App


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()


app = App(node_id='test', loop=loop)


@app.timer(interval=1)
async def timer_test():
    date_now = datetime.now()
    print(date_now)
