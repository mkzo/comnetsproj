import sys
from packet import *
from routingtables import *

routing_table = routing_tables("r4")
interface_table = interface_tables("r4")

r4_r7_socket = socket(AF_INET, SOCK_DGRAM)
r4_r7_socket.bind(('192.168.1.15', 8902))
while True:
    data, addr = r4_r7_socket.recvfrom(1024)
    if data:
        pkttypestr = pkttype_string(data)
        log_write("Router 4 R7Socket: Received " + pkttypestr + " packet from source " + str(addr[0]) + "\n")
        
        route_packet(data, routing_table, interface_table, "Router 4 R7Socket: ")
