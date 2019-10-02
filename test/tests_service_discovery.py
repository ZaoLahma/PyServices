import unittest
import socket
import struct
import json

import core
from core.service_discovery_listener import ServiceDiscoveryListener
from core.service_discovery_scheduler import ServiceDiscoveryScheduler
from core.service_discovery_config import ServiceDiscoveryConfig
from core.service_discovery_handler import ServerRunner
from core.service_discovery_handler import ServerFactory
from core.service_nw_misc import ServiceNwMisc

class ServiceDiscoveryListenerTest(unittest.TestCase):

    def setUp(self):
        self.config = ServiceDiscoveryConfig("./test/test.cfg")
        self.listener = ServiceDiscoveryListener(self.config)
        self.service_scheduler = ServiceDiscoveryScheduler(self.config)
        self.service_scheduler.register_runnable(self.listener)
        self.service_scheduler.start(own_thread = True)

        self.server_scheduler = ServiceDiscoveryScheduler(self.config)
        self.server = ServerFactory.create_server(self.config)
        self.server_runner = ServerRunner(self.server)
        self.server_scheduler.register_runnable(self.server_runner)
        self.server_scheduler.start(own_thread = True)

    def tearDown(self):
        print("tearDown")
        self.service_scheduler.stop()
        self.server_scheduler.stop()

    def test_service_discovery(self):
        service_discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ttl = struct.pack('b', 1)
        service_discovery_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        request = '{"request" : "locate-service-handler"}'
        multicast_group = ("224.3.29.71", 8081)

        try:
            sent = service_discovery_socket.sendto(request.encode(), multicast_group)
            self.assertFalse(sent == 0)
            response = service_discovery_socket.recv(4096)
            print("Response: {}".format(response.decode()))
            response = json.loads(response.decode())
            port_no = response["response"]["port-no"]
            self.assertIsNot(port_no, -1)

        finally:
            service_discovery_socket.close()

    def test_register_and_get_service(self):
        try:
            service_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            own_ip = ServiceNwMisc.get_own_ip()
            service_socket.connect((own_ip, 8088))
            service_socket.sendall('{"request" : {"service" : "register-service", "value" : {"name" : "test-service", "version" : 1, "address" : "127.0.0.1", "port-no" : 9999}}}\r\n'.encode())
            response = service_socket.recv(4096)
            print("Response test_register_service: {}".format(response))
            response = json.loads(response.decode())
            print("json response: {}".format(response))
            self.assertEqual("added", response["response"]["register-service"]["result"])

            service_socket.sendall('{"request" : {"service" : "get-service", "value" : {"name" : "test-service", "version" : 1}}}\r\n'.encode())
            response = service_socket.recv(4096)
            response = json.loads(response)
            self.assertEqual(9999, response["response"]["get-service"]["result"]["port-no"])
            self.assertEqual("127.0.0.1", response["response"]["get-service"]["result"]["address"])

        finally:
            service_socket.close()

if "__main__" == __name__:
    unittest.main()