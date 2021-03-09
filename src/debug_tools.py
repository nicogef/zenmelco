import timeit

class CodeTimer(object):
    def __init__(self, name):
        self.name = name
        self.logs = []
    
    def log(self, name):
        took = (timeit.default_timer() - self.start) * 1000000.0
        self.logs.append("{:>15} - {:8.0f} us".format(self.name, took))
        self.reset(name)

    def reset(self, name):
        self.start = timeit.default_timer()
        self.name = name if name else ""

    def __enter__(self):
        self.reset(self.name)
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.log(None)
        print("\n".join(self.logs))