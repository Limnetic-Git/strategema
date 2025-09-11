import pysocknet
import random
from _thread import *
from map import World
from units import UnitsList, Scout

world_seed = random.randint(0, 999999)
world = World(seed=world_seed)
units_list = UnitsList()
world.spawn_teams(4, units_list)

TreadCount = 0
print(world_seed)
def TCPThread(connection):
    global TreadCount
    first_pack = {'world_seed': world_seed,
                        'id': TreadCount}
    TreadCount += 1
    TCPChannel.send(connection, f'{first_pack}')
    while True:
        incoming_pack = TCPChannel.receive(connection, 20480, raw=False)
        TCPChannel.send(connection, 'Hi, and i am server! (TCP)')
        
def UDPThread():
    while True:
        incoming_pack, addr = UDPChannel.receive(2048, raw=True)
        pack = str(units_list.pack_units_list())
        UDPChannel.send(addr, f'{pack}')
    

TCPChannel = pysocknet.TCPServerConnection('127.0.0.1', 1234)
UDPChannel = pysocknet.UDPServerConnection('127.0.0.1', 1235)


start_new_thread(TCPChannel.start_client_accepting_loop, (TCPThread,))
start_new_thread(UDPThread, ())

