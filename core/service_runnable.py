class ServiceRunnable:
    def run(self):
        raise NotImplementedError

    def stop(self):
        print("Default stop")

    def de_init(self):
        print("Default de_init")