import sys
from socket import socket, AF_INET, SOCK_DGRAM
from routingtables import *
from packet import *

rttbl = routing_tables("host")

d1_socket = socket(AF_INET, SOCK_DGRAM)
d1_socket.bind((rttbl[101][0], rttbl[101][1]))
while True:
    data, addr = d1_socket.recvfrom(1024)
    if data:
        pkttypestr = pkttype_string(data)
        log_write("Dest 1: Received " + pkttypestr + " packet from source " + str(addr[0]) + "\n")
