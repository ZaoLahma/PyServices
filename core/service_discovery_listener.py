import socket
import struct
import sys
import json

class ServiceDiscoveryListener:
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

    def run(self):
        try:
            data = self.multicast_socket.recvfrom(4096)
        except  socket.timeout:
            pass
        except:
            raise
        else:
            print("Data: {}".format(data))
            data = json.loads(data[0].decode())
            service = data["request"]["service"]
            version = data["request"]["version"]
            print("ServiceDiscoveryListener received {} - {}".format(service, version))