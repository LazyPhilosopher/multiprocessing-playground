import uuid


class Task:
    def __init__(self, func: callable, args: list = None, kwargs: dict = None, max_executions: int = 1):
        self.id: uuid = uuid.uuid4()
        self.func: callable = func
        self.args: list = args
        self.kwargs: dict = kwargs
        self.result = None

        self.max_executions = max_executions
        self.rank = 1

    def unpack(self):
        return self.func, self.args, self.kwargs
