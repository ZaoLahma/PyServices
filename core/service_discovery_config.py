import json

class ServiceDiscoveryConfig:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config = None
        with open(config_file_path, 'r') as f:
            self.config = json.load(f)

    def get_config(self, config_group, config_name):
        return self.config[config_group][config_name]["value"]