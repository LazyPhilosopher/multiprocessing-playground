import multiprocessing
import threading
import queue

class BaseServiceModule:
    def __init__(self, name, process_count=1):
        self.name = name
        self.process_count = process_count
        self.processes = []
        self.input_queue = multiprocessing.Queue()
        self.result_queue = multiprocessing.Queue()
        self.running = multiprocessing.Event()
        self.running.set()

    def start(self):
        for _ in range(self.process_count):
            p = multiprocessing.Process(target=self._process_loop)
            p.start()
            self.processes.append(p)

    def stop(self):
        self.running.clear()
        for _ in self.processes:
            self.input_queue.put(None)
        for p in self.processes:
            p.join()

    def _process_loop(self):
        def worker(func, args, sender):
            result = func(**args) if args else func()
            if sender:
                sender.put(result)

        while self.running.is_set():
            try:
                task = self.input_queue.get(timeout=0.1)
                if task is None:
                    break
                func, args, sender = task
                threading.Thread(target=worker, args=(func, args, sender), daemon=True).start()
            except queue.Empty:
                continue

    def send_request(self, func, args=None, sender=None):
        self.input_queue.put((func, args, sender))
