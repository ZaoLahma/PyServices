class ServiceHandler:
    def __init__(self, config):
        self.config = config
        self.services = {}

    def handle_request(self, request):
        service = request["request"]["service"]
        version = request["request"]["version"]

        known_service = False
        try:
            if version in self.services[service]:
                known_service = True

        if False == known_service:        
            print("ServiceHandler received request for unknow service {} ({})".format(service, version))
            
    def register_service(self, service, version):
        try:
            self.services[service]
        except KeyError:
            self.services[service] = []
        self.services[service].append(version)

