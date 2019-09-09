import unittest
import socket
import struct

import core
from core.service_discovery_listener import ServiceDiscoveryListener
from core.service_discovery_scheduler import ServiceDiscoveryScheduler
from core.service_discovery_config import ServiceDiscoveryConfig

class ServiceDiscoveryListenerTest(unittest.TestCase):

    def setUp(self):
        self.config = ServiceDiscoveryConfig("./test/test.cfg")
        self.listener = ServiceDiscoveryListener(self.config)
        self.scheduler = ServiceDiscoveryScheduler(self.config)
        self.scheduler.register_runnable(self.listener)
        self.scheduler.start(own_thread = True)

    def test_service_discovery(self):
        service_discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ttl = struct.pack('b', 1)
        service_discovery_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        request = '{"request" : {"service" : "test", "version" : 1}}'
        multicast_group = ("224.3.29.71", 8081)

        try:
            sent = service_discovery_socket.sendto(request.encode(), multicast_group)
        finally:
            service_discovery_socket.close()

        self.scheduler.stop()

if "__main__" == __name__:
    unittest.main()