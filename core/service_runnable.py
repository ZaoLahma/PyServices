class ServiceRunnable:
    def run(self):
        raise NotImplementedError

    def de_init(self):
        print("Default de_init")