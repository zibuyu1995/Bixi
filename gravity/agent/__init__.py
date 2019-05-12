# coding: utf-8


from mode import Service


class Agent(Service):
    func = None

    def __init__(self, func, *, channel=None, **kwargs):
        self.func = func
        super().__init__()

    def actor_from_stream(self):
        return {}

    def __call__(self, *args, **kwargs):
        return self.actor_from_stream()





