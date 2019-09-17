import socket

class ServiceHandlerListener:
    def __init__(self, config):
        self.config = config
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        port_no = self.config.get_config("service-port-numbers", "1")

        self.server_socket.bind(('', port_no))
        self.server_socket.settimeout(0.001)

    def run(self):
        try:
            new_connection = self.server_socket.accept()
        except socket.timeout:
            pass
        except:
            raise
        else:
            print("ServiceHandlerListener connected to by {}".format(new_connection))