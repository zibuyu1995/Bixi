import asyncio

import uvloop

from mtasks.app import App


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()


app = App(node_id='test', loop=loop)


@app.timer(interval=1)
async def timer_test():
    print('timer_test')


@app.crontab(cron_format='18 * * * *')
async def crontab_test():
    print('crontab_test')
