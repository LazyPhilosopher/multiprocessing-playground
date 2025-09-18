# base_service_module.py
import multiprocessing
import threading
import queue
import uuid

from core.logger.logger import Logger
from core.struct.task import Task

logger_config = Logger()
module_logger = logger_config.get_logger("default")


class BaseServiceModule:
    """Module service base class.
    Module runs in its own process and periodically checks task queue for execution.
    Once task is found a new thread is started to both execute task and keep module from freezing.
    """
    def __init__(self, name, result_storage=None):
        self.name = name
        self.input_queue = multiprocessing.Queue()
        self.running = multiprocessing.Event()
        self.running.set()
        self.result_storage = result_storage  # Store reference to the shared result storage
        self.max_threads = multiprocessing.Value('i', 3)

    def start(self):
        """Start module process."""
        # for _ in range(self.process_count):
        p = multiprocessing.Process(target=self._process_loop)
        p.start()

    def stop(self):
        """Stop module process."""
        self.running.clear()
        # for _ in range(self.process_count):
        # self.input_queue.put(None)

    def set_max_threads(self, max_threads: int):
        self.max_threads.value = max_threads

    def _process_loop(self):
        """Check module task queue for execution."""
        running_threads = {}

        def worker(_key: uuid, _task: Task):
            # Task execution class wrapper
            result = _task.func(**_task.kwargs) if _task.kwargs else _task.func()
            if result is not None:
                if isinstance(result, Exception):
                    if _task.max_executions > 1:
                        module_logger.warning(f"Scheduling task {_key} for re-execution")
                        _task.max_executions -= 1
                        self.send_request(_task, key=_key)
                    else:
                        module_logger.error(f"Failed to execute task {_key}.")
                        self.result_storage.put_result(_key=_key, _value=result)
                else:
                    self.result_storage.put_result(_key=_key, _value=result)


        while self.running.is_set():
            removal_keys = []
            for result_key in running_threads.keys():
                if result_key in self.result_storage.results:
                    removal_keys.append(result_key)
                    _value = self.result_storage.results[result_key]
            [running_threads.pop(_key) for _key in removal_keys]

            try:
                if len(running_threads) >= self.max_threads.value:
                    # print(f"{self.max_threads.value}??")
                    continue

                key, task = self.input_queue.get(timeout=0.1)
                # Check task queue
                if task is None:
                    break
                # Task queue item is expected to contain tuple of result key, function and its arguments.
                # Once finished, function result is put into Master module result queue with result key as reference.
                # key, func, args = task
                # Start task execution thread
                thread = threading.Thread(target=worker, args=(key, task), daemon=True).start()
                running_threads[key] = thread
            except queue.Empty:
                continue

    def send_request(self, task: Task, key: uuid = None):
        """Send module for method execution."""
        if not key:
            key = uuid.uuid4()
        self.input_queue.put((key, task))
        return key
