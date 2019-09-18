import socket

class ServiceNwMisc:
    @staticmethod
    def get_own_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('5.255.255.255', 1))
        IP = s.getsockname()[0]
        s.close()
        return IP