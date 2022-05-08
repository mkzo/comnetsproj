import sys
from socket import socket, AF_INET, SOCK_DGRAM
from routingtables import *
from packet import *

rttbl = routing_tables("host")

d3_socket = socket(AF_INET, SOCK_DGRAM)
d3_socket.bind((rttbl[103][0], rttbl[103][1]))
while True:
    data, addr = d3_socket.recvfrom(1024)
    if data:
        pkttypestr = pkttype_string(data)
        log_write("Dest 3: Received " + pkttypestr + " packet from source " + str(addr[0]) + "\n")
