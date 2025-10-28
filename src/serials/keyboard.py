import time
import threading


class Keyboard(threading.Thread):
    def __init__(self, input_queue):
        super().__init__(daemon=True)
        self._q = input_queue

    def run(self):
        while True:
            key = input(">> ")
            self._q.put(key)
            time.sleep(0.1)