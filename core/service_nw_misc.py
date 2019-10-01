import socket

class ServiceNwMisc:
    IP = None
    @staticmethod
    def get_own_ip():
        if None == ServiceNwMisc.IP:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('5.255.255.255', 1))
            ServiceNwMisc.IP = s.getsockname()[0]
            s.close()
        return ServiceNwMisc.IP