import pysocknet
from _thread import *


class ClientConnection:
    def __init__(self, ip, port):
        self.TCPChannel = pysocknet.TCPClientConnection(ip, port)
        self.UDPChannel = pysocknet.UDPClientConnection(ip, port+1)
        
        self.tasks = []
        self.tasks_id_counter = 0
        
        self.world_seed = None
        self.id = None
        self.units_dict = None
        self.world_changes = []
        
        start_new_thread(self.TCPThread, ())
        start_new_thread(self.UDPThread, ())
        while self.world_seed == None: pass
        
    def TCPThread(self):
        first_pack = self.TCPChannel.receive(20480, raw=False)
        self.world_seed = first_pack['world_seed']
        self.id = first_pack['id']
        while True:
            tasks_pack = self.tasks.copy()
            pack = {'id': self.id, 'tasks': tasks_pack}
            if tasks_pack != []:
                print(pack)
            self.TCPChannel.send(f'{pack}')
            
            incoming_pack = self.TCPChannel.receive(20480, raw=False)
            for i in incoming_pack:
                self.world_changes.append(i)
            
            self.tasks = ([] if self.tasks == tasks_pack else self.tasks)
            
    def UDPThread(self):
        while True:
            try:
                self.UDPChannel.send('Hello! My name is Client (UDP)')
                incoming_pack = self.UDPChannel.receive(204800, raw=False)
                if incoming_pack != None:
                    self.units_dict = incoming_pack
            except Exception as e:
                print(e)




