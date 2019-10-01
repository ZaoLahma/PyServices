import socket
import struct
import sys
import json

from .service_nw_misc import ServiceNwMisc
from .service_runnable import ServiceRunnable

class ServiceDiscoveryListener(ServiceRunnable):
    def __init__(self, config):
        print("Init called")
        self.config = config

        multicast_address = self.config.get_config("network", "multicast-address")
        multicast_port_no = self.config.get_config("network", "multicast-port-no")

        multicast_server_address = ("", multicast_port_no)

        group = socket.inet_aton(multicast_address)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        
        self.multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.multicast_socket.bind(multicast_server_address)
        self.multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.multicast_socket.settimeout(0.001)

        self.own_ip = ServiceNwMisc.get_own_ip()

    def run(self):
        try:
            data = self.multicast_socket.recvfrom(4096)
        except  socket.timeout:
            pass
        except:
            raise
        else:
            print("Data: {}".format(data))
            request = json.loads(data[0].decode())
            client_request = request["request"]

            port_no = None
            try:
                port_no = self.config.get_config(client_request, "port-no")
            except KeyError:
                port_no = -1

            print("ServiceDiscoveryListener - Returning {} on port_no: {}".format(self.own_ip, port_no))

            response = {}
            response["response"] = {}
            response["response"]["port-no"] = port_no
            response["response"]["address"] = self.own_ip

            response = json.dumps(response)

            client_endpoint = data[1]
            response_socket = None
            try:
                response_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                response_socket.sendto(response.encode(), client_endpoint)
            finally:
                response_socket.close()

    def de_init(self):
        print("de_init listener")
        self.multicast_socket.close()
                