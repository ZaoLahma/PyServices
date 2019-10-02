import socketserver
import threading
import json

from .service_nw_misc import ServiceNwMisc
from .service_runnable import ServiceRunnable

# Oof... Ugly
global_config = None

class ServerRunner(ServiceRunnable):
    def __init__(self, server):
        self.server = server

    def run(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()

    def de_init(self):
        print("de_init ServerRunner")
        self.server.server_close()

class ServerFactory:
    @staticmethod
    def create_server(config):
        print("create_server called")

        global global_config
        if None == global_config:
            global_config = config

        handler_ip_address = ServiceNwMisc.get_own_ip()
        handler_port_no = config.get_config("locate-service-handler", "port-no")

        return ServiceHandlerServer((handler_ip_address, handler_port_no), ServiceHandler)

class ServiceHandlerServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

class ServiceHandler(socketserver.StreamRequestHandler):
    # Decode and route request. 
    # Only two possibilities - register service or get service
    def handle(self):
        client = f'{self.client_address} on {threading.currentThread().getName()}'
        print(f'Connected: {client}')

        data = None
        while True:
            data = self.rfile.readline()
            response = None
            try:
                data_json = json.loads(data.decode("utf-8"))

                request = data_json["request"]
                service = request["service"]

                if "register-service" == service:
                    response = self.handle_register_service(request)
                    print("ServiceHandler - Response {}".format(response))
                elif "get-service" == service:
                    response = self.handle_get_service(request)
            except:
                print("ServiceHandler - Failed to decode {}".format(data))

            if None != response:
                self.wfile.write((response + "\r\n").encode("utf-8"))
            if not data:
                break

        print("Received: {}".format(data))
    
    # Set new service information in the config
    def handle_register_service(self, request):
        print("ServiceHandler - handle_register_service")
        service_data = request["value"]
        service_name = service_data["name"]
        service_version = service_data["version"]
        service_address = service_data["address"]
        service_port_no = service_data["port-no"]

        global global_config
        global_config.add_service(service_name, service_version, service_address, service_port_no)

        print("ServiceHandler - Service data:\r\n{}".format(service_data))

        return '{"response" : {"register-service" : {"result" : "added"}}}'

    # Lookup service in config
    def handle_get_service(self, request):
        print("ServiceHandler - handle_get_service")
        service_name = request["value"]["name"]
        service_version = request["value"]["version"]

        response = None
        global global_config
        fail = True
        try:
            service = global_config.get_config("services", service_name)
            if service["version"] == service_version:
                response = {}
                response["response"] = {}
                response["response"]["get-service"] = {}
                response["response"]["get-service"]["result"] = {}
                response["response"]["get-service"]["result"]["address"] = service["address"]
                response["response"]["get-service"]["result"]["port-no"] = service["port-no"]
                response = json.dumps(response)
                fail = False
        except KeyError:
            fail = True
        
        if fail:
            print("ServiceHandler - Service {} ({}) not found".format(service_name, service_version))
            response = '{"response" : {"get-service" : {"result" : {"address" : "", "port-no": -1}}}'

        print("Response: {}".format(response))

        return response


