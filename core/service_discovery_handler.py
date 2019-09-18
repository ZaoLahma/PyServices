import socketserver
import threading
import json

from .service_nw_misc import ServiceNwMisc
from .service_runnable import ServiceRunnable

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

        handler_ip_address = ServiceNwMisc.get_own_ip()
        handler_port_no = config.get_config("locate-service-handler", "port-no")

        return ServiceHandlerServer((handler_ip_address, handler_port_no), ServiceHandler)

class ServiceHandlerServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

class ServiceHandler(socketserver.StreamRequestHandler):
    def handle(self):
        client = f'{self.client_address} on {threading.currentThread().getName()}'
        print(f'Connected: {client}')

        data = None
        while True:
            data = self.rfile.readline()

            try:
                data_json = json.loads(data.decode("utf-8"))

                request = data_json["request"]
                service = request["service"]
                print("ServiceHandler - Received request for service: {}".format(service))
                service_data = request["value"]
                print("ServiceHandler - Service data:\r\n{}".format(service_data))
            except:
                print("ServiceHandler - Failed to decode {}".format(data))

            print("data_json: {}".format(data_json))

            self.wfile.write("RESPONSE\r\n".encode("utf-8"))
            if not data:
                break

        print("Received: {}".format(data))

