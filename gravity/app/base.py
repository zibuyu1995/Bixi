# coding: utf-8

from mode import Service
from itertools import chain


class App(Service):

    def __init__(self, node_id, *, loop=None):
        self.finalized = False
        self.node_id = node_id
        super().__init__(loop=loop)

    def on_init_dependencies(self):
        servers = chain(
            self.producer(),
            self.consumer(),
            self.web_server()
        )
        return servers

    async def on_start(self):
        if not self.finalized:
            self.finalized = True

    def producer(self):
        ...

    def consumer(self):
        ...

    def web_server(self):
        ...

    def chanel(self):
        ...

