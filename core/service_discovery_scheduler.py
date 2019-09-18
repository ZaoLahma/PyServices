import time
from threading import Thread
from threading import Lock

class ServiceDiscoveryScheduler(Thread):
    def __init__(self, config):
        Thread.__init__(self)
        self.config = config
        self.runnables = []
        self.active = False
        self.exec_lock = Lock()
        self.own_thread = False

    def run(self):
        print("Scheduler start")
        self.active = True
        while self.active:
            sched_periodicity = self.config.get_config("system", "sched-periodicity")
            with self.exec_lock:
                for runnable in self.runnables:
                    runnable.run()
                    time.sleep(sched_periodicity)
        print("Scheduler stop")


    def start(self, own_thread = False):
        self.own_thread = own_thread
        if True == self.own_thread:
            Thread.start(self)
        else:
            self.run()

    def stop(self):
        self.active = False
        if True == self.own_thread:
            runnables_copy = self.runnables
            for runnable in runnables_copy:
                self.remove_runnable(runnable)
            self.join()

    def register_runnable(self, runnable):
        self.runnables.append(runnable)

    def remove_runnable(self, runnable):
        print("Removing runnable {}".format(runnable))
        runnable.stop()
        with self.exec_lock:
            self.runnables.remove(runnable)
        runnable.de_init()