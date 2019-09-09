from core.service_discovery_config import ServiceDiscoveryConfig
from core.service_discovery_listener import ServiceDiscoveryListener
from core.service_discovery_scheduler import ServiceDiscoveryScheduler

import argparse

class Main:
    @staticmethod
    def run(config_file_path):
        print("Run called")
        config = ServiceDiscoveryConfig(config_file_path)
        listener = ServiceDiscoveryListener(config)
        scheduler = ServiceDiscoveryScheduler(config)
        scheduler.register_runnable(listener)

        scheduler.start()
        
if "__main__" == __name__:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-cfg", help="The config file")
    args = arg_parser.parse_args()
    
    config_file_path = args.cfg
    
    Main.run(config_file_path)