import socket
import ast
from _thread import *
import logging
logging.basicConfig(level=logging.INFO, filename="log.txt", filemode="w")

class TCPClientConnection:
    def __init__(self, ip: str, port: int):
        try:
            self.ip = ip
            self.port = port
            self.ClientSocket = socket.socket()
            self.__connect()
            logging.info(f"TCP-client socket ({self.ip}:{self.port}) has been successfully created")

        except socket.error as e:
            logging.error(e)
            raise e

    def __connect(self):
        try:
            self.ClientSocket.connect((self.ip, self.port))
        except socket.error as e:
            logging.error(e)
            raise e

    def receive(self, packet_size: int, raw=False):
        try:
            received_data = self.ClientSocket.recv(packet_size).decode('utf-8')
            if raw:
                return received_data
            else:
                return ast.literal_eval(received_data)
        except socket.error as e:
            logging.error(e)
            raise e
        
    def send(self, packet: str):
        try:
            self.ClientSocket.send(str.encode(packet))
        except socket.error as e:
            logging.error(e)
            raise e
        
    def close(self):
        try:
            self.ClientSocket.close()
        except socket.error as e:
            logging.error(e)
            raise e
        
class TCPServerConnection:
    def __init__(self, ip: str, port: int, max_peers_count=100):
        try:
            self.ip = ip
            self.port = port
            self.max_peers_count = max_peers_count
            self.ServerSocket = socket.socket()
            self.__connect()
            logging.info(f"TCP-server socket ({self.ip}:{self.port}) has been successfully created")

        except socket.error as e:
            logging.error(e)
            raise e
        
    def __connect(self):
        try:
            self.ServerSocket.bind((self.ip, self.port))
            self.ServerSocket.listen(self.max_peers_count) 
        except socket.error as e:
            logging.error(e)
            raise e
        
    def start_client_accepting_loop(self, func):
        while True:
            try:
                Client, address = self.ServerSocket.accept()
                start_new_thread(func, (Client,))
                logging.info(f"Created connection with {address[0]}:{address[1]}")
            except socket.error as e:
                logging.error(e)
                raise e
        
    def receive(self, connection, packet_size: int, raw=False):
        try:
            received_data = connection.recv(packet_size).decode('utf-8')
            if raw:
                return received_data
            else:
                return ast.literal_eval(received_data)
        except socket.error as e:
            logging.error(e)
            raise e
        
    def send(self, connection, packet: str):
        try:
            connection.send(str.encode(packet))
        except socket.error as e:
            logging.error(e)
            raise e
        
    def accept(self):
        try:
            Client, address = self.ServerSocket.accept()
            logging.info(f"Created connection with {address[0]}:{address[1]}")
            return Client, address
        
        except socket.error as e:
            logging.error(e)
            raise e
        
    def close(self):
        try:
            self.ServerSocket.close()
        except socket.error as e:
            logging.error(e)
            raise e    
    
class UDPClientConnection:
    def __init__(self, ip: str, port: int):
        try:
            self.ip = ip
            self.port = port
            self.ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.ClientSocket.bind(('0.0.0.0', 0))
            self.ClientSocket.settimeout(0.25)
            logging.info(f"UDP-client socket ({self.ip}:{self.port}) has been successfully created")

        except socket.error as e:
            logging.error(e)
            raise e
        
    def receive(self, packet_size: int, raw=False):
        try:
            received_data, _ = self.ClientSocket.recvfrom(packet_size)
            if raw:
                return received_data.decode('utf-8')
            else:
                return ast.literal_eval(received_data.decode('utf-8'))
        except socket.timeout:
            pass
        
        except Exception as e:
            logging.error(e)
            raise e
        
    def send(self, packet: str):
        try:
            self.ClientSocket.sendto(str.encode(packet), (self.ip, self.port))
        except socket.error as e:
            logging.error(e)
            raise e
        
    def close(self):
        try:
            self.ClientSocket.close()
        except socket.error as e:
            logging.error(e)
            raise e
        
class UDPServerConnection:
    def __init__(self, ip: str, port: int):
        try:
            self.ip = ip
            self.port = port
            self.ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.__connect()
            logging.info(f"UDP-server socket ({self.ip}:{self.port}) has been successfully created")

        except socket.error as e:
            logging.error(e)
            raise e
        
    def __connect(self):
        try:
            self.ServerSocket.bind((self.ip, self.port))
        except socket.error as e:
            logging.error(e)
            raise e
        
    def receive(self, packet_size: int, raw=False):
        try:
            data, addr = self.ServerSocket.recvfrom(packet_size)
            if raw:
                return data.decode('utf-8'), addr
            else:
                return ast.literal_eval(data.decode('utf-8')), addr
        except socket.error as e:
            logging.error(e)
            raise e
        
    def send(self, addr, packet: str):
        try:
            self.ServerSocket.sendto(str.encode(packet), addr)
        except socket.error as e:
            logging.error(e)
            raise e
        
    def close(self):
        try:
            self.ServerSocket.close()
        except socket.error as e:
            logging.error(e)
            raise e