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
            print("Data: {}".format(data.decode("utf-8")))

            self.wfile.write("RESPONSE\r\n".encode("utf-8"))
            if not data:
                break

        print("Received: {}".format(data))

