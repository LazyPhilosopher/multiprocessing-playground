import uuid
from typing import Generic, TypeVar, ParamSpec, Callable

P = ParamSpec("P")
R = TypeVar("R")


class Task(Generic[P, R]):
    def __init__(self, func: Callable[P, R], max_reexecutions: int = 1, *args: P.args, **kwargs: P.kwargs):
        self.id: uuid = uuid.uuid4()
        self.func: callable = func
        self.args: list = args
        self.kwargs: dict = kwargs
        self.result: R | None = None

        self.max_executions = max_reexecutions
        self.rank = 1

    def unpack(self):
        return self.func, self.args, self.kwargs

    def execute(self) -> R | None:
        if self.args and self.kwargs:
            return self.func(*self.args, **self.kwargs)
        elif self.args:
            return self.func(*self.args)
        elif self.kwargs:
            return self.func(**self.kwargs)
        else:
            return self.func()
