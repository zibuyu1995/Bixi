from bixi.app import App


app = App(node_id='task')


@app.task
async def task_test():
    print('task_test')

