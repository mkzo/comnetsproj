import sys
from socket import socket, AF_INET, SOCK_DGRAM
from routingtables import *
from packet import *

rttbl = routing_tables("host")

d2_socket = socket(AF_INET, SOCK_DGRAM)
d2_socket.bind((rttbl[102][0], rttbl[102][1]))
while True:
    data, addr = d2_socket.recvfrom(1024)
    if data:
        pkttypestr = pkttype_string(data)
        log_write("Dest 2: Received " + pkttypestr + " packet from source " + str(addr[0]) + "\n")

