import pysocknet
from _thread import *

def TCPThread(connection):
    global players, client_id
    players = TCPChannel.receive(20480, raw=False)
    client_id = players[-1]['id']
    print(f'My client id: {client_id}')
    while True:
        TCPChannel.send('Hello! My name is Client (TCP)')
        string = TCPChannel.receive(20480, raw=True)
        print(string)
        
def UDPThread():
    while True:
        UDPChannel.send('Hello! My name is Client (UDP)')
        string = UDPChannel.receive(20480, raw=True)
        print(string)
        
TCPChannel = pysocknet.TCPClientConnection('127.0.0.2', 1234)
UDPChannel = pysocknet.UDPClientConnection('127.0.0.2', 1235)

players = []
client_id = None
start_new_thread(TCPThread, (TCPChannel,))
start_new_thread(UDPThread, ())
