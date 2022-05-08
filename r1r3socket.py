import sys
from packet import *
from routingtables import *

routing_table = routing_tables("r1")
interface_table = interface_tables("r1")

r1_r3_socket = socket(AF_INET, SOCK_DGRAM)
r1_r3_socket.bind(('192.168.1.5', 8892))
while True:
    data, addr = r1_r3_socket.recvfrom(1024)
    if data:
        pkttypestr = pkttype_string(data)
        log_write("Router 1 R3Socket: Received " + pkttypestr + " packet from source " + str(addr[0]) + "\n")
        
        route_packet(data, routing_table, interface_table, "Router 1 R3Socket: ")
