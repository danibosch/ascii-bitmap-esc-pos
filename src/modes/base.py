import wrappers.base as wrappers


class BaseMode:
    def __init__(self, printer, wrapper):
        self.printer = printer
        if wrapper is not None:
            self.wrapper = getattr(wrappers, wrapper.replace("_", "").title())()
        else:
            self.wrapper = None

    def run(self):
        pass