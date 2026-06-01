# A simple client-server library.
#version 1.0_A
import socket
class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))

    def send_message(self, message):
        self.client_socket.sendall(message.encode())

    def receive_message(self):
        return self.client_socket.recv(1024).decode()

    def close(self):
        self.client_socket.close()
    def wait_for_response(self):
        response = self.client_socket.recv(1024).decode()
        while not response:
            response = self.client_socket.recv(1024).decode()
        return response
class server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)

    def accept_connection(self):
        self.client_socket, self.client_address = self.server_socket.accept()
        print(f"Connection from {self.client_address}")

    def receive_message(self):
        return self.client_socket.recv(1024).decode()

    def send_message(self, message):
        self.client_socket.sendall(message.encode())

    def close(self):
        self.client_socket.close()
        self.server_socket.close()
    def wait_for_message(self):
        message = self.receive_message()
        while not message:
            message = self.receive_message()
        return message
if __name__ == "__main__":
    print("online_lib module run directly. Import this module to use client/server classes.")
    print('Try again!')