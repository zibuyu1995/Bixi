from bixi.app import App


app = App(node_id='timer')


@app.timer(interval=1)
async def timer_test():
    print('timer_test')


@app.crontab(cron_format='18 * * * *')
async def crontab_test():
    print('crontab_test')
