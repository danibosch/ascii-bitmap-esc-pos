import src.wrappers.base as wrappers


class BaseMode:
    def __init__(self, printer, wrapper, input_queue):
        self._q = input_queue
        self.printer = printer
        if wrapper is not None:
            self.wrapper = getattr(wrappers, wrapper)()
        else:
            self.wrapper = None

    def run(self):
        pass