import sys
from packet import *
from routingtables import *

routing_table = routing_tables("r3")
interface_table = interface_tables("r3")

r3_r4_socket = socket(AF_INET, SOCK_DGRAM)
r3_r4_socket.bind(('192.168.1.9', 8896))
while True:
    data, addr = r3_r4_socket.recvfrom(1024)
    if data:
        pkttypestr = pkttype_string(data)
        log_write("Router 3 R4Socket: Received " + pkttypestr + " packet from source " + str(addr[0]) + "\n")
        
        route_packet(data, routing_table, interface_table, "Router 3 R4Socket: ")
        
