import json

class ServiceDiscoveryConfig:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config = None
        with open(config_file_path, 'r') as f:
            self.config = json.load(f)

    def get_config(self, config_group, config_name):
        return self.config[config_group][config_name]["value"]

    def add_service(self, service_name, service_version, service_port_no):
        try:
            service_config = {}
            service_config[service_name] = {}
            service_config[service_name]["value"] = {}
            service_config[service_name]["value"]["version"] = service_version
            service_config[service_name]["value"]["port-no"] = service_port_no
            self.config["services"].update(service_config)
        except Exception as e:
            print("FAILED: {}".format(e))

        print("ServiceDiscoveryConfig - add_service new config: {}".format(self.config))