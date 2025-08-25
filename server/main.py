import pysocknet
import random
from _thread import *

players = []


def TCPThread(connection):
    players.append({'id': len(players)})
    while True:
        TCPChannel.send(connection, f'{players}')
        string = TCPChannel.receive(connection, 20480, raw=True)
        print(string)
        TCPChannel.send(connection, 'Hi, and i am server! (TCP)')
        
def UDPThread():
    while True:
        string, addr = UDPChannel.receive(20480, raw=True)
        print(string)
        UDPChannel.send(addr, 'Hello, im Server! (UDP)')
    

TCPChannel = pysocknet.TCPServerConnection('127.0.0.2', 1234)
UDPChannel = pysocknet.UDPServerConnection('127.0.0.2', 1235)


start_new_thread(TCPChannel.start_client_accepting_loop, (TCPThread,))
start_new_thread(UDPThread, ())
