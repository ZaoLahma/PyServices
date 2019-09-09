import time
from threading import Thread

class ServiceDiscoveryScheduler(Thread):
    def __init__(self, config):
        Thread.__init__(self)
        self.config = config
        self.runnables = []
        self.active = False

    def run(self):
        self.active = True
        while self.active:
            sched_periodicity = self.config.get_config("system", "sched-periodicity")
            for runnable in self.runnables:
                runnable.run()
                time.sleep(sched_periodicity)

    def start(self, own_thread = False):
        if True == own_thread:
            Thread.start(self)
        else:
            self.run()

    def stop(self):
        self.active = False

    def register_runnable(self, runnable):
        self.runnables.append(runnable)