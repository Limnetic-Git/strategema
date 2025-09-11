import pysocknet
from _thread import *

class ClientConnection:
    def __init__(self, ip, port):
        self.TCPChannel = pysocknet.TCPClientConnection(ip, port)
        self.UDPChannel = pysocknet.UDPClientConnection(ip, port+1)
        
        self.world_seed = None
        self.id = None
        self.units_dict = None
        
        start_new_thread(self.TCPThread, (self.TCPChannel,))
        start_new_thread(self.UDPThread, ())
        while self.world_seed == None: pass
        
        
        
    def TCPThread(self, connection):
        first_pack = self.TCPChannel.receive(20480, raw=False)
        self.world_seed = first_pack['world_seed']
        self.id = first_pack['id']
        while True:
            pack = {'id': self.id}
            self.TCPChannel.send(f'{pack}')
            incoming_pack = self.TCPChannel.receive(20480, raw=True)
            
    def UDPThread(self):
        while True:
            self.UDPChannel.send('Hello! My name is Client (UDP)')
            self.units_dict = self.UDPChannel.receive(204800, raw=False)

    


