import asyncio

import click
import uvloop
from mode import Worker

from gravity.utils.base import symbol_by_name, import_from_cwd


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()


@click.group()
@click.option('--app', '-A', help='gravity app')
@click.pass_context
def main(ctx, app):
    ctx.obj['app'] = app


@main.command()
@click.pass_context
def run(ctx):
    app = ctx.obj['app']
    _init_worker(app)


def start():
    main(obj={})


def _init_worker(app_name):
    app = symbol_by_name(app_name, imp=import_from_cwd)
    worker = Worker(app, loglevel="info", loop=app.loop)
    worker.execute_from_commandline()


if __name__ == '__main__':
    start()
